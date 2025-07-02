import random
from faker import Faker
from django.core.management.base import BaseCommand
from ...models import Category, Product, Author

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with example data'

    def add_arguments(self, parser):
        parser.add_argument('--num_categories', type=int, default=5, help='Number of categories to create')
        parser.add_argument('--num_products', type=int, default=20, help='Number of products to create')  # переименовали
        parser.add_argument('--num_authors', type=int, default=10, help='Number of authors to create')

    def handle(self, *args, **kwargs):
        num_categories = kwargs['num_categories']
        num_products = kwargs['num_products']
        num_authors = kwargs['num_authors']

        # Создаем категории
        categories = []
        for _ in range(num_categories):
            category = Category.objects.create(name=fake.word())
            categories.append(category)

        # Создаем продукты
        products = []
        for _ in range(num_products):  # Изменили переменную
            category = random.choice(categories)
            product = Product.objects.create(
                name=fake.word(),
                description=fake.sentence(),
                price=round(random.uniform(1000, 5000), 2),
                stock=random.randint(1, 100),  # Добавляем stock, если он есть
                category=category
            )
            products.append(product)  # Сохраняем созданный продукт

        # Создаем авторов и связываем их с продуктами
        for _ in range(num_authors):
            author = Author.objects.create(name=fake.name())
            # Случайное число продуктов для данного автора
            num_products_to_sample = random.randint(1, min(5, len(products)))

            if num_products_to_sample > 0:
                selected_products = random.sample(products, num_products_to_sample)
                author.product.set(selected_products)  # Установим выбранные продукты
            else:
                print(f"Для автора {author.name} не найдено продуктов.")

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {num_categories} categories, {num_products} products, and {num_authors} authors'))