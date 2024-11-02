# admin.py
from django.contrib import admin
from .models import Transaction, Network

admin.site.register(Transaction)
admin.site.register(Network)
