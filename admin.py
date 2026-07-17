from django.contrib import admin
from .models import Product, Box


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'length', 'width', 'height', 'weight']
    search_fields = ['name']


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['name', 'inner_length', 'inner_width', 'inner_height', 'max_weight', 'cost']
    search_fields = ['name']
    ordering = ['cost']
