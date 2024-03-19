from django.contrib import admin
from .models import Carousel,Category
from .models import Product
from .models import UserProfileTable


# Register your models here.
admin.site.register(Carousel)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserProfileTable)