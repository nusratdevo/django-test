import django_filters
from .models import Product, ProductVariant

class ProductFilter(django_filters.FilterSet):                            # Stockfilter used to filter based on name
    title = django_filters.CharFilter(lookup_expr='icontains')   
    updated_at = django_filters.DateTimeFilter(lookup_expr='icontains')        # allows filtering without entering the full name
    class Meta:
        model = Product
        fields = ['title','updated_at' ]

    def get_all_attr_variants(self) :
         variants = ProductVariant.objects.filter(product=self)
         return variants