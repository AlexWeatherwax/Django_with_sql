from django.shortcuts import render, get_object_or_404
from book_sales.models import Product

def product_list(request):
    products = Product.objects.all()
    products_for_sale = [product for product in products if product.stock!= 0]
    not_sale = [product for product in products if product.stock== 0]

    context =dict(products = products_for_sale, not_sale = not_sale)

    return render(request, 'product_list.html', context)

def book_detail(request, pk):  # pk - первичный ключ книги
    book = get_object_or_404(Product, pk=pk)
    return render(request, 'book_detail.html', {'book': book})