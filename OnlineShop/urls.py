"""
URL configuration for OnlineShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page,name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),  # You need to create this view
    path('shop/', views.form_page, name='shop_page'),
    path('cart/', views.cart_page, name='cart'),
    path('profile/', views.profile, name='profile'),
    path('fetch-numbers/', views.fetch_numbers, name='fetch_numbers'),
    path('add/',views.add_to_cart, name='add_to_cart'),
    path('update-quantity/', views.update_quantity, name='update_quantity'),
    path('delete-document/', views.deleteProduct, name='delete_document'),
    path('update_quantity_slider/',views.update_quantity_slider, name='update_slider'),
    path('update_quantity_input/',views.update_quantity_input, name='update_input'),
    path('sort_documents/', views.sort_documents, name='sort_documents'),
    path('send-email/', views.send_email, name='send_email'),
    path('catalog/', views.catalog_view, name='catalog'),

    path('get_current_page_values/', views.get_current_page_products, name='get_page_values'),
    path('add_to_cart_from_catalog/', views.add_to_cart_from_catalog, name='add_from_catalog'),

    # path('finish_order/', )



]
