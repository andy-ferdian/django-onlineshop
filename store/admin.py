from django.contrib import admin

# Register your models here.
from . models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductVariationInline]
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductColor)
admin.site.register(ProductCategory)
admin.site.register(ProductSize)
admin.site.register(ProductVariation)
admin.site.register(ShippingFrom)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
