from django.test import TestCase
from .factories import CategoryFactory, ProductFactory, AuthorFactory
from .services import get_product_for_sale

class ModelsTestCase(TestCase):

    def setUp(self):
        # Создаем несколько категорий
        self.category1 = CategoryFactory.create(name='Books')
        self.category2 = CategoryFactory.create(name='Stationery')

        # Создаем несколько продуктов
        self.product1 = ProductFactory.create(
            name='Bookmark',
            category=self.category1,
            price=1500.00,
            stock=100
        )
        self.product2 = ProductFactory.create(
            name='Notebook',
            category=self.category2,
            price=2500.00,
            stock=200
        )

    def test_product_creation(self):
        """Проверяем создание продукта."""
        self.assertEqual(self.product1.name, 'Bookmark')
        self.assertEqual(self.product1.price, 1500.00)
        self.assertEqual(self.product1.stock, 100)
        self.assertEqual(self.product1.category.name, 'Books')

    def test_author_with_products(self):
        """Проверяем, что автор может иметь продукты."""
        author = AuthorFactory.create(name='Test Author')
        author.product.add(self.product1)
        author.product.add(self.product2)

        self.assertEqual(author.product.count(), 2)
        self.assertIn(self.product1, author.product.all())
        self.assertIn(self.product2, author.product.all())

    def test_product_relation_with_category(self):
        """Проверяем связь между продуктом и категорией."""
        self.assertEqual(self.product1.category, self.category1)
        self.assertEqual(self.product2.category, self.category2)

    def test_author_creation_with_random_products(self):
        """Проверяем создание автора с случайными продуктами."""
        author = AuthorFactory.create()  # Создайте автора без передачи продуктов

        # Создаем случайные продукты
        product1 = ProductFactory.create()
        product2 = ProductFactory.create()

        # Добавляем созданные продукты к автору
        author.product.add(product1)
        author.product.add(product2)

        # Проверяем, что автор имеет продукты
        self.assertEqual(author.product.count(), 2)  # Теперь должно быть 2
        self.assertIn(product1, author.product.all())
        self.assertIn(product2, author.product.all())

    def test_category_string_representation(self):
        """Проверяем, что строковое представление категории корректно."""
        self.assertEqual(str(self.category1), 'Books')
        self.assertEqual(str(self.category2), 'Stationery')

    def test_product_string_representation(self):
        """Проверяем, что строковое представление продукта корректно."""
        self.assertEqual(str(self.product1), 'Bookmark')
        self.assertEqual(str(self.product2), 'Notebook')

    def test_author_string_representation(self):
        """Проверяем, что строковое представление автора корректно."""
        self.assertEqual(str(AuthorFactory.create(name='John Doe')), 'John Doe')

class ProductServiceTestCase(TestCase):

    def setUp(self):
        # Создаем несколько категорий
        self.category1 = CategoryFactory.create(name='Books')
        self.category2 = CategoryFactory.create(name='Stationery')

        # Создаем несколько продуктов с различным количеством на складе
        self.product_in_stock = ProductFactory.create(name='In Stock Product', category=self.category1, stock=10)
        self.product_out_of_stock = ProductFactory.create(name='Out of Stock Product', category=self.category2, stock=0)
        self.product_in_stock_2 = ProductFactory.create(name='Another In Stock Product', category=self.category1, stock=5)

    def test_get_product_for_sale(self):
        """Проверяем, что функция возвращает правильный контекст для продуктов на продаже."""
        context = get_product_for_sale()

        # Проверяем, что продукты на продаже возвращаются корректно
        self.assertIn(self.product_in_stock, context['products'])
        self.assertIn(self.product_in_stock_2, context['products'])
        self.assertNotIn(self.product_out_of_stock, context['products'])

        # Проверяем, что недоступные продукты возвращаются корректно
        self.assertIn(self.product_out_of_stock, context['not_sale'])

        # Проверяем количество продуктов в контексте
        self.assertEqual(len(context['products']), 2)  # Два продукта на продаже
        self.assertEqual(len(context['not_sale']), 1)  # Один недоступный продукт
