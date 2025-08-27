from decimal import Decimal

from django import forms
from django.contrib import admin, messages
from django.db.models import Count
from django.core.exceptions import PermissionDenied
from .models import Category, Product, Merch, Author, Message, Review


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ()


    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'name') and isinstance(obj.name, str):
            obj.name = obj.name.strip()
        super().save_model(request, obj, form, change)


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название товара',
                'style': 'width: 60%;'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'style': 'width: 80%;'
            }),
            'category': forms.Select(attrs={'style': 'min-width: 200px;'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': 0}),
            'stock': forms.NumberInput(attrs={'min': 0}),
        }


# Кастомный фильтр по остаткам
class LowStockFilter(admin.SimpleListFilter):
    title = 'остаток'
    parameter_name = 'stock_level'

    def lookups(self, request, model_admin):
        return (
            ('zero', '0 (нет на складе)'),
            ('low', '< 10 (мало)'),
            ('ok', '>= 10 (достаточно)'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'zero':
            return queryset.filter(stock=0)
        if value == 'low':
            return queryset.filter(stock__gt=0, stock__lt=10)
        if value == 'ok':
            return queryset.filter(stock__gte=10)
        return queryset


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    form = ProductAdminForm

    list_display = ('id', 'name', 'category', 'price', 'stock', 'is_published')
    list_filter = ('is_published', LowStockFilter)
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_published')

    actions = ['publish_products', 'unpublish_products', 'discount_10_percent']

    # Ограничиваем действие правом can_publish
    def publish_products(self, request, queryset):
        if not request.user.has_perm('your_app_label.can_publish'):
            raise PermissionDenied("Недостаточно прав для публикации.")
            updated = queryset.update(is_published=True)
            self.message_user(request, f'Опубликовано товаров: {updated}', level=messages.SUCCESS)

    def unpublish_products(self, request, queryset):
        if not request.user.has_perm('your_app_label.can_publish'):
            raise PermissionDenied("Недостаточно прав для публикации.")
            updated = queryset.update(is_published=False)
            self.message_user(request, f'Снято с публикации: {updated}', level=messages.SUCCESS)

    def discount_10_percent(self, request, queryset):
        for obj in queryset:
            obj.price = (obj.price * Decimal('0.90')).quantize(Decimal('0.01'))
            obj.save(update_fields=['price'])
        self.message_user(request, 'Скидка 10% применена к выбранным товарам', level=messages.INFO)
    discount_10_percent.short_description = 'Сделать скидку 10%%'

    # Проверка пользовательского права для действий
    # Замените 'your_app_label' на реальный label вашего приложения (см. apps.py или имя папки)
    def has_can_publish_permission(self, request, obj=None):
        return request.user.has_perm('book_sales.can_publish')

    # Специфическая логика сохранения для Product:
    #  - цена не может быть отрицательной
    #  - если stock <= 0, автоматически снимаем с публикации
    def save_model(self, request, obj, form, change):
        if obj.price is not None and obj.price < 0:
            obj.price = Decimal('0.00')
        if obj.stock is not None and obj.stock <= 0:
            obj.is_published = False
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('id', 'name', 'products_count')
    search_fields = ('name',)

    # Показать число связанных товаров, оптимизировано через аннотацию
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(num_products=Count('product'))

    def products_count(self, obj):
        return getattr(obj, 'num_products', obj.product_set.count())
    products_count.short_description = 'Товаров'


@admin.register(Merch)
class MerchAdmin(BaseAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Author)
class AuthorAdmin(BaseAdmin):
    list_display = ('id', 'name', 'products_count')
    filter_horizontal = ('product',)
    search_fields = ('name',)

    def products_count(self, obj):
        return obj.product.count()
    products_count.short_description = 'Товаров'


@admin.register(Message)
class MessageAdmin(BaseAdmin):
    list_display = ('id', 'name', 'is_chat_message', 'created_at')
    list_filter = ('is_chat_message', 'created_at')
    search_fields = ('name', 'message')
    readonly_fields = ('created_at',)


@admin.register(Review)
class ReviewAdmin(BaseAdmin):
    list_display = ('id', 'product', 'name', 'short_message')
    list_filter = ('product',)
    search_fields = ('name', 'message', 'product__name')

    def short_message(self, obj):
        return (obj.message[:50] + '...') if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Сообщение'