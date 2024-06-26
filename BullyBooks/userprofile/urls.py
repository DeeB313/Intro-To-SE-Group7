from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="userprofile/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('myaccount/', views.my_account, name='my_account'),
    path('my-items/', views.my_items, name='my_items'),
    path('my-items/order-details/<int:pk>/', views.my_items_order_detail, name='my_items_order_detail'),
    path('my-items/add-items/', views.add_items, name='add_items'),
    path('my-items/edit-items/<int:pk>/', views.edit_items, name='edit_items'),
    path('my-items/delete-items/<int:pk>/', views.delete_items, name='delete_items'),
    path('seller/<int:pk>/', views.seller_detail, name='seller_detail'),
    path('user_management/', views.user_management, name='user_management'),
    path('change_status/<str:username>/', views.change_status, name='change_status'),
]