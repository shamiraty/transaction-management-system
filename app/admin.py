from django.contrib import admin
from .models import Network, Transaction, Tax, ProductCategory, Product, Sales, SoldProduct

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 20

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'network', 'action', 'customer', 'amount', 'phonenumber', 'created_date')
    list_filter = ('action', 'created_date', 'network')
    date_hierarchy = 'created_date'
    list_per_page = 20

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_collection',)
    list_per_page = 20

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 20

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'purchasing_price', 'selling_price', 'tax_collection', 'expected_profit', 'barcode', 'expiry_date', 'category')
    list_filter = ('category', 'expiry_date')
    date_hierarchy = 'created_at'
    list_per_page = 20

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ('product', 'profit', 'user', 'created_at')
    list_filter = ('created_at', 'product')
    date_hierarchy = 'created_at'
    list_per_page = 20

@admin.register(SoldProduct)
class SoldProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'purchasing_price', 'selling_price', 'expected_profit', 'barcode', 'expiry_date', 'category', 'profit', 'user', 'created_at')
    list_filter = ('category', 'expiry_date', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 20
