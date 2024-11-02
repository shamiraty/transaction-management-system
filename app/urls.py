from django.urls import path
from . import views
from .views import *

urlpatterns = [
    
    #create transaction
    path('create/', views.transaction_create, name='transaction_create'),  # Page for creating a new transaction
    #list of transactions
    path('transactions/', transaction_list, name='transaction_list'),
    #when table item is clicked for view
    path('transactions/<int:pk>/', transaction_detail, name='transaction_detail'),
    #when table item is clicked for update
    path('transactions/<int:pk>/edit/', transaction_update, name='transaction_update'),   
    #when table item is clicked for delete
    path('transactions/<int:pk>/delete/', transaction_delete, name='transaction_delete'), 
    #analytics
    path('', transaction_summary, name='transaction_summary'),
        
]
