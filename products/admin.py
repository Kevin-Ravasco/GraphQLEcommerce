from django.contrib import admin

from products.models import Category, Product, ProductMedia


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'timestamp']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'quantity', 'date_updated', 'date_added']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'timestamp']
    list_filter = ['product']
