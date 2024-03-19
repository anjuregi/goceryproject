from django import template
from groceryapp.models import *
register = template.Library()

@register.filter()
def applydiscount(pid):
    data = Product.objects.get(id=pid)
    price = int(data.price) * (100 - int(data.discount))/100
    return price