from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('user/', views.userPage, name="user-page"),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name='customer'),

    path('account/', views.accountSettings, name="account"),

    path('issued-books', views.issuedBooks, name='issuedBooks'),
    path('late-submissions', views.lateSubmissions, name='lateSubmissions'),
    path('returned-books', views.returnedBooks, name='returnedBooks'),

    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),

    path('contactus/', views.contactPage, name='contactus'),
]