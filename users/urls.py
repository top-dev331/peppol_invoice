from django.urls import path
from .views import home, send_invoice, profile, RegisterView
from . import views

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('sendinvoice/', send_invoice, name='send-invoice'),
    path('setting/', views.profile_and_customers, name='profile_and_customers'),
    path('setting/edit/<int:pk>/', views.edit_customer, name='edit_customer'),
    path('setting/delete/<int:pk>/', views.delete_customer, name='delete_customer'),
]
