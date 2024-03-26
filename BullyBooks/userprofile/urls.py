from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="userprofile/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('myaccount/', views.my_account, name='my_account'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('seller/<int:pk>/', views.seller_detail, name='seller_detail'),

]