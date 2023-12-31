import ast

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from shop.forms import UserRegisterForm

json_file_path = os.path.join(settings.BASE_DIR,"shop", "static", "key2.json")
cred = credentials.Certificate(json_file_path)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()



def home_page(request):
    return render(request, 'home.html')

@login_required
def form_page(request):
    documents = []
    search_term=''
    if request.method == 'POST':
        search_term = request.POST.get('number').upper()

        db = firestore.client()
        query = db.collection('item').where('name', '==', search_term)
        documents = query.stream()

    cart = get_cart(request)
    quantity = 1
    inside = False
    for prod in cart:
        if search_term == prod['name']:
            inside = True
            quantity = prod['quantity']
            break

    context = {
        'documents': [doc.to_dict() for doc in documents],
        'search_term': search_term,
        'inside': inside,
        'quantity': quantity,
        'is_authenticated': 'False',
        'in_cart': 'False'
    }

    return render(request, 'shop_page.html', context)
@login_required
def cart_page(request):
    context = {
        'documents': sorted(get_cart(request), key=lambda x: x['number'])
    }
    return render(request, 'cart.html', context=context)

def fetch_numbers(request):
    search_term = request.GET.get('term', '').lower()
    numbers = []

    if search_term != '':
        # Using Firestore query to filter documents
        name_query = db.collection('item').where('name', '>=', search_term).where('name', '<=',
                                                                                  search_term + '\uf8ff').stream()

        # Filter the results in Python for the 'quantity' field
        numbers = [doc.to_dict().get('name', '') for doc in name_query if
                   search_term in doc.to_dict().get('name', '').lower() and
                   doc.to_dict().get('quantity', 0) > 0]

    return JsonResponse(numbers, safe=False)
# Create your views here.
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product = ast.literal_eval(data.get('document'))

        email = request.user.email  # Replace with actual user email
        print(email)
        quantity = 1  # Replace with actual quantity
        price = product['price']  # Replace with actual price
        name = product['name']  # Replace with actual product name
        image = product['image-url']
        maximum_quantity = product['quantity']
        description = product['description']

        cart_ref = db.collection("Cart")

        cart_items = cart_ref.where('emailOwner', '==', email).get()
        cart_size = len(cart_items)
        item_number = cart_size + 1

        new_cart_item = {
            'description':description,
            "emailOwner": email,
            'image_url': image,
            "name": name,
            "price": price,
            "quantity": quantity,
            "number": item_number,
            'quantity_max': maximum_quantity
        }
        cart_ref.add(new_cart_item)

        return JsonResponse({'status': 'success', 'quantity': quantity,  'number': item_number, 'sum':price})
    return JsonResponse({'status': 'error'}, status=400)
def update_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity_change = data.get('quantity_change')  # Will be 1 or -1
        document = ast.literal_eval(data.get('document'))
        quantity_max = 0
        try:
            quantity_max = document['quantity_max']
        except:
            quantity_max = document['quantity']

        cart_ref = db.collection('Cart')

        # Get current quantity and update
        email = request.user.email
        docs = cart_ref.where('emailOwner', '==', email).where('name', '==', product_id).limit(1).stream()
        for doc in docs:
            current_quantity = doc.to_dict().get('quantity', 0)
            new_quantity = max(current_quantity + quantity_change, 1)  # Ensure quantity doesn't go below 0
            if new_quantity<= quantity_max:

                doc.reference.update({'quantity': new_quantity})

                return JsonResponse({'status': 'success', 'quantity': new_quantity, 'sum': "€"+str(round(new_quantity * document['price'],1))})
            else:
                return JsonResponse({'status': 'error', 'message': 'You have reached maximum quantity'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
def update_quantity_slider(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity_new = data.get('quantity_new')
        document = data.get('document')

        cart_ref = db.collection('Cart')

        # Get current quantity and update
        email = request.user.email
        docs = cart_ref.where('emailOwner', '==', email).where('name', '==', product_id).limit(
            1).stream()
        for doc in docs:
            # Update the quantity in Firestore
            doc.reference.update({'quantity': int(quantity_new)})
            sum_value = round(float(quantity_new) * float(document['price']), 2)
            return JsonResponse(
                {'status': 'success', 'quantity': quantity_new, 'product_id': product_id, 'sum': "€"+str(sum_value)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
def update_quantity_input(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity_new = data.get('quantity_new')
        price = float(data.get('price'))

        cart_ref = db.collection('Cart')

        # Get current quantity and update
        email = request.user.email
        docs = cart_ref.where('emailOwner', '==', email).where('name', '==', product_id).limit(1).stream()
        for doc in docs:
            doc.reference.update({'quantity': int(quantity_new)})
            return JsonResponse({'status': 'success', 'quantity': quantity_new, 'product_id': product_id, 'sum': "€"+str(round((quantity_new * price),2))})

        else:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
def get_cart(request):
    # Access the Firebase database

    cart_ref = db.collection('Cart')
    email = request.user.email
    # Get all the documents
    docs = cart_ref.where('emailOwner', '==', email).stream()

    cart = []
    for doc in docs:
        cart.append({'name':doc.to_dict().get('name'),'quantity':doc.to_dict().get('quantity'),'number':doc.to_dict().get('number'), 'image_url':doc.to_dict().get('image_url'), 'description':doc.to_dict().get('description'),'quantity_max':doc.to_dict().get('quantity_max'),'price':doc.to_dict().get('price'), 'sum':str(round(doc.to_dict().get('price')*doc.to_dict().get('quantity'),1))})
    return cart
def deleteProduct(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('document_id')
        cart_ref = db.collection('Cart')
        email = request.user.email
        docs = cart_ref.where('emailOwner', '==', email).where('name', '==', name).stream()
        for doc in docs:
            doc.reference.delete()

        remaining_docs = cart_ref.where('emailOwner', '==', email).order_by('number').stream()
        new_number = 1
        updated_documents = []
        for doc in remaining_docs:
            doc.reference.update({'number': new_number})
            updated_documents.append({'id': doc.to_dict().get('name',''), 'number': new_number})
            new_number += 1

        return JsonResponse({'status': 'success', 'updated_documents': updated_documents})
    return JsonResponse({'status': 'error'}, status=400)
def sort_documents(request):
    order_by = request.GET.get('order_by', 'name')
    direction = request.GET.get('direction', 'asc')

    # Get documents from Firebase
    documents = get_cart(request)
    print(documents)
    if order_by == 'sum':
        key_function = lambda x: x.get('price', 0) * x.get('quantity', 0)
    else:
        key_function = lambda x: x.get(order_by, "")

    sorted_documents = sorted(documents, key=key_function, reverse=(direction == 'desc'))

    print(sorted_documents)
    return JsonResponse({'documents': sorted_documents})

def register(request):
    form= UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form, 'errors': form.errors})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('home')
def send_email(request):
    if request.method == 'POST':
        # Define email parameters
        subject = 'Test mail'
        message = 'Test mail from order-form!'
        recipient_list = ['eramcheg@gmail.com']  # replace with your recipient list

        # Send the email
        send_mail(subject, message, 'setting.EMAIL_HOST_USER', recipient_list)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)