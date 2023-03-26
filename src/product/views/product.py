import json
from django.http import HttpResponse
from django.views import generic
from django.views.generic import ListView
from product.models import Product, ProductVariant, ProductVariantPrice, Variant
from product.filters import ProductFilter
from django_filters.views import FilterView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        product_variants = ProductVariantPrice.objects.all()
        context['product'] = True
        context['variants'] = list(variants.all())
        context['product_variants'] = product_variants
        return context
 

  


class LIstProductView(FilterView,ListView):
    model = Product
    filterset_class = ProductFilter
    template_name = 'products/list.html'
    context_object_name = 'product'
    paginate_by = 2

    

    def get_queryset(self):
        filter_string = {}
        min = 0
        max = 0
        variant =''
        print(self.request.GET)
        allProducts=Product.objects.all().order_by('-id').distinct()

        if self.request.GET.get('price_from') and self.request.GET.get('price_to') :                
                max = self.request.GET.get('price_to')
                min = self.request.GET.get('price_from')
               
                allProducts=allProducts.filter(product_price__price=min)
                allProducts=allProducts.filter(product_price__price=max)
        elif self.request.GET.get('variant'):
                variant = self.request.GET.get('variant')
                allProducts=allProducts.filter(product_variant__variant_title=variant)
                # return Product.product_price.filter(price__range=(int(min),int(max) ))
        return allProducts

    def get_context_data(self, **kwargs):
        context = super(LIstProductView, self).get_context_data(**kwargs)
        variants_list = list(ProductVariantPrice.objects.all().values_list('product_variant_one','product_variant_two'))
        context['variants'] = Variant.objects.filter(active=True)
        context ['product_variants'] = ProductVariantPrice.objects.all()
        context ['variants_list'] = (variants_list)
        return context
    
@csrf_exempt
def ProductSave(request):
         # product save in  products model
        data =  request.POST
        save_product = Product(title=data['title'], sku=data['sku'], description = data['description'])
        save_product.save()
                      
        product_price = ProductVariantPrice(product_variant_one=data['productVariants'][0], product=save_product, product_variant_two = data['productvariant'][1], price = data['productVariantsPrices']['price'], stock = data['productVariantsPrices']['stock'])
        product_price.save()
        messages.success(request, 'Product Successfully saved.')
        return HttpResponse(json.dumps(messages),content_type='application/json')