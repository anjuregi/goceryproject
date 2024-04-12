"""
URL configuration for groceryproject project.

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
from django.conf.urls.static import static
from django.urls import path,include
from django.conf import settings
from groceryapp.views import Navigation,Index,About,Home
from groceryapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('nav/', Navigation.as_view(),name="navigation"),
    path('about/', About.as_view(),name="about"),
    path('', Home,name="home"),
    path('index/', Index, name="index"),
    path('admin_login/', adminLogin, name="admin_login"),
    path('admin_base/', adminHome, name="admin_base"),
    path('admindashboard/', admin_dashboard, name="admindashboard"),
    path('add-category/', add_category, name="add_category"),
    path('view-category/', view_category, name="view_category"),
    path('edit-category/<int:pk>/', edit_category, name="edit_category"),
    path('delete-category/<int:pk>/', delete_category, name="delete_category"),
    path('add-product/', add_product, name='add_product'),
    path('view-product/', view_product, name='view_product'),
    path('edit-product/<int:pk>/', edit_product, name="edit_product"),
    path('delete-product/<int:pk>/', delete_product, name="delete_product"),
    path('registration/', registration, name="registration"),
    path('userlogin/', userlogin, name="userlogin"),
    path('profile/', profile, name="profile"),
    path('logout/', logoutuser, name="logout"),
    path('change_password/', change_password, name="change_password"),
    path('user-product/<int:pid>/', user_product, name="user_product"),
    path('product-detail/<int:pid>/', product_detail, name="product_detail"),
    path('add-to-cart/<int:pid>/', addToCart, name="addToCart"),
    path('cart/', cart, name="cart"),
    path('incredecre/<int:pid>/', incredecre, name="incredecre"),
    path('deletecart/<int:pid>/', deletecart, name="deletecart"),
    path('booking/', booking, name="booking"),
    path('my-order/', myOrder, name="myorder"),
    path('user-order-track/<int:pid>/', user_order_track, name="user_order_track"),
    path('change-order-status/<int:pid>/', change_order_status, name="change_order_status"),
    path('user_feedback/', user_feedback, name="user_feedback"),
    path('manage-feedback/', manage_feedback, name="manage_feedback"),
    path('delete-feedback/<int:pid>/', delete_feedback, name="delete_feedback"),
    path('payment/', payment, name="payment"), 
    path('feedback-read/<int:pid>/', read_feedback, name="read_feedback"),
    path('manage-order/', manage_order, name="manage_order"), 
    path('delete-order/<int:pid>/', delete_order, name="delete_order"), 
    path('admin-order-track/<int:pid>/', admin_order_track, name="admin_order_track"),
    path('manage-user/', manage_user, name="manage_user"),
    path('delete-user/<int:pid>/', delete_user, name="delete_user"),
    path('admin-change-password/',admin_change_password, name="admin_change_password"),
    path('contact/', contact, name="contact"),
    path('delivery_registration/', delivery_registration, name="delivery_registration"),
    path('delivery/', delivery, name="de_home"),
    path('delivery_manage_order/', delivery_manage_order, name="delivery_manage_order"),
    path('delivery_delete_order/<int:pid>', delivery_delete_order, name="delivery_delete_order"),
    path('delivery_order_track/<int:pid>', delivery_order_track, name="delivery_order_track"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
