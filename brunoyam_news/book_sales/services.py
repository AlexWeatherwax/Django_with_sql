from .models import Merch

def get_most_expensive_merch():
    return Merch.objects.filter(price__gt=2000).order_by('-price').first()