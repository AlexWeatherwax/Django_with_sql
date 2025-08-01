from django.shortcuts import render, get_object_or_404, redirect
from .services import get_product_for_sale
from .models import Product
from .forms import MessageForm, ReviewForm
from .models import Message, Review
from django.core.paginator import Paginator


def product_list(request):
    context =get_product_for_sale()
    products = context['products']
    paginator = Paginator(products, 10)  # 10 продуктов на странице
    page_number = request.GET.get('page')  # Номер страницы из параметров запроса
    page_obj = paginator.get_page(page_number)  # Получаем продукты для текущей страницы

    # Формируем список страниц для отображения
    page_range = list(paginator.page_range)
    context['page_obj'] = page_obj
    context['page_range'] = page_range  # Передаем диапазон страниц в контекст
    return render(request, 'product_list.html', context)

def chat_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if not message.name.strip():  # Установка имени по умолчанию на "Аноним"
                message.name = "Аноним"
            message.is_chat_message = True  # Установка флага, чтобы обозначить как сообщение чата
            message.save()
            return redirect('contact')  # Перенаправление на страницу чата

    else:
        form = MessageForm()

    # Получение всех сообщений, относящихся к чату
    chat_messages = Message.objects.filter(is_chat_message=True).order_by('-created_at')

    return render(request, 'contact.html', {
        'form': form,
        'chat_messages': chat_messages,
    })

def product_detail(request, pk):
    book = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=book).order_by('-id')

    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = book
            review.name = form.cleaned_data.get('name')  # Получаем имя из формы
            review.save()
            return redirect('product_detail', pk=book.pk)
    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'book': book,
        'form': form,
        'page_obj': page_obj,
    })
