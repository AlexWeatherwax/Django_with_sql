from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_published = models.BooleanField(default=False)
    class Meta:
        permissions = [
            ('can_publish', 'Может публиковать статьи'),
        ]

    def __str__(self):
        return self.name

class Merch(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    product = models.ManyToManyField(Product, related_name="author")
    def __str__(self):
        return self.name

class Message(models.Model):
    name = models.CharField(max_length=100, blank=True)  # Имя отправителя, может быть пустым для анонимных сообщений
    message = models.TextField()  # Текст сообщения
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания сообщения
    is_chat_message = models.BooleanField(default=False)  # Флаг для определения, является ли это сообщением чата

    def __str__(self):
        return self.message

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)  # Поле не обязательно для заполнения
    message = models.TextField()

    def __str__(self):
        return self.name if self.name else "Аноним"

