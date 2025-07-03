from .models import Merch, Product

def get_most_expensive_merch():
    return Merch.objects.filter(price__gt=2000).order_by('-price').first()

def get_product_for_sale():
    products = Product.objects.all()
    products_for_sale = [product for product in products if product.stock!= 0]
    not_sale = [product for product in products if product.stock== 0]
    context =dict(products = products_for_sale, not_sale = not_sale)
    return context