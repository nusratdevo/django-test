from django.contrib import admin

from product.models import Product, ProductVariant, Variant, ProductVariantPrice

# Register your models here.

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['variant_title','variant','product']
 
class ProductVariantPriceAdmin(admin.ModelAdmin):
    list_display = ['product_variant_one','product_variant_two','product', 'price','stock']
    

class ProductVariantInLineAdmin(admin.TabularInline):
    model = ProductVariant
    extra = 1
class VariantAdmin(admin.ModelAdmin):
    list_display = ['title','description' ]
    list_filter = ['title']
    search_fields = ['title']
    inlines = [ProductVariantInLineAdmin]


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','description']
    list_filter = ['title']
    search_fields = ['title']
    
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariantPrice, ProductVariantPriceAdmin)