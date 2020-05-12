from django.contrib import admin

from .models import AirProduct, Producer, Category

# Register your models here.
admin.site.register(AirProduct)
admin.site.register(Producer)
admin.site.register(Category)