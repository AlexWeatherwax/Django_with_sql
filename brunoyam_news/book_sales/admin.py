from django.contrib import admin
from .models import Category, Product, Merch, Author, Contact, ChatMessage

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Merch)
admin.site.register(Author)
admin.site.register(Contact)
admin.site.register(ChatMessage)

