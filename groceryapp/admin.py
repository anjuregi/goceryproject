from django.contrib import admin
from .models import Carousel,Category
from .models import Product
from .models import UserProfileTable,Cart,Booking,Feedback,DeliveryProfileTable


# Register your models here.
admin.site.register(Carousel)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserProfileTable)
admin.site.register(Cart)
admin.site.register(Booking)
admin.site.register(Feedback)
admin.site.register(DeliveryProfileTable)