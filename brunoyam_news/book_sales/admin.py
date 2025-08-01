from django.contrib import admin
from .models import Category, Product, Merch, Author, Review, Message

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Merch)
admin.site.register(Author)
admin.site.register(Message)
admin.site.register(Review)

