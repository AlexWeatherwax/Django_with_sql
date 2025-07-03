from django.shortcuts import render, get_object_or_404
from .services import get_product_for_sale
from .models import Product

def product_list(request):
    context =get_product_for_sale()
    return render(request, 'product_list.html', context)

def book_detail(request, pk):  # pk - первичный ключ книги
    book = get_object_or_404(Product, pk=pk)
    return render(request, 'book_detail.html', {'book': book})