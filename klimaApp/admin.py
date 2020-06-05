from django.contrib import admin

from .models import AirProduct, Producer, Category, Contact, Valuation, Profil, Order, Cart, CartProducts

# Register your models here.
admin.site.register(AirProduct)
admin.site.register(Producer)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Valuation)
admin.site.register(Profil)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartProducts)