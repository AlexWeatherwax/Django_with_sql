import factory
from faker import Faker
from .models import Author, Product, Category
fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')  # Используем 'word' для названия категории

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')  # Используем 'word' для названия продукта
    category = factory.SubFactory(CategoryFactory)  # Связываем с категорией
    description = factory.Faker('text')
    price = factory.Faker('random_number', digits=3)
    stock = factory.Faker('random_int', min=0, max=100)

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker('name')

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        """Добавляет продукты к автору, если они были переданы."""
        if not create:
            return

        if extracted:
            # Продукты переданы явно, добавляем их
            for product in extracted:
                self.product.add(product)
        else:
            # Если не передано, случайный продукт не добавляется
            pass




