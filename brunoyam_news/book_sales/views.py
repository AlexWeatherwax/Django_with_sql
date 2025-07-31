from django.shortcuts import render, get_object_or_404, redirect
from .services import get_product_for_sale
from .models import Product
from .forms import ContactForm, ChatMessageForm, ReviewForm
from .models import Contact, ChatMessage, Review
from django.core.paginator import Paginator
from django.contrib import messages

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

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()  # Сохранение данных в базе данных

            # Создание отдельного сообщения для чата
            chat_message = ChatMessage(contact=contact, text=contact.message)
            chat_message.save()

            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return redirect('contact')  # Перенаправление на ту же страницу
    else:
        form = ContactForm()
    chat_messages = ChatMessage.objects.all().order_by('-created_at')  # Получаем все сообщения для отображения

    return render(request, 'contact.html', {'form': form, 'chat_messages': chat_messages})

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
