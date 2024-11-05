from django.urls import path
from . import views
from .views import *

urlpatterns = [
    
    #create transaction
    path('create_product/', views.transaction_create, name='transaction_create'),  # Page for creating a new transaction
  
    #list of transactions
    path('transactions/', transaction_list, name='transaction_list'),
    
    #when table item is clicked for view
    path('transactions/<int:pk>/', transaction_detail, name='transaction_detail'),
    
    #when table item is clicked for update
    path('transactions/<int:pk>/edit/', transaction_update, name='transaction_update'),
       
    #when table item is clicked for delete
    path('transactions/<int:pk>/delete/', transaction_delete, name='transaction_delete'), 
    
    #transaction analytics
    path('', transaction_summary, name='transaction_summary'),
    
    #add product
    path('add_product/', add_product_batch, name='add_product'),
    
    #list products
    path('products/', product_list, name='product_list'),
    
    #sale
    path('create/', create_sale, name='create_sale'),
    
    #sold products, update, delete and view
    path('sold_products/', views.sold_product_list, name='sold_product_list'),
    path('sold_product/<int:pk>/detail/', views.sold_product_detail, name='sold_product_detail'),
    path('sold_product/<int:pk>/update/', views.update_sold_product, name='update_sold_product'),
    path('sold_product/<int:pk>/delete/', views.delete_sold_product, name='delete_sold_product'),
    
    #products, update, delete and view
    path('products_view/', views.product_list_view, name='product_list_view'),
    path('products/<int:pk>/detail/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'), 
    
    #product tends
     path('analytics/', analytics_page, name='analytics'), 

]
