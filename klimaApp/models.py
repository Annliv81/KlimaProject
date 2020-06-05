from django.db import models
from django.contrib.auth.models import User

# Create your models here.

COLORS = (
    (1, "black"),
    (2, "white"),
    (3, "antracyt"),
    (4, "red"),
    (5, "blue")
)

class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa kategorii')

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=64, verbose_name='Producent')

    def __str__(self):
        return self.name

class AirProduct(models.Model):
    name = models.CharField(max_length=128, verbose_name="Nazwa:")
    color=models.IntegerField(choices=COLORS, null=True, verbose_name="Kolor:")
    description = models.TextField(verbose_name="Opis:")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena:")
    available = models.BooleanField(default=True, verbose_name="Dostępność:")
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, verbose_name="Kategoria:")
    producer = models.ForeignKey(Producer, null=True, on_delete=models.CASCADE, verbose_name="Producent:")
    foto = models.ImageField(upload_to='klima_image', height_field=None, width_field=None, max_length=100, null=True, verbose_name="Zdjęcie:")
    #biblioteka  pip install Pillow

    def __str__(self):
        return self.name

class Contact(models.Model):
    first_name = models.CharField(max_length=128, verbose_name='Imię')
    last_name = models.CharField(max_length=128, verbose_name='Nazwisko')
    mail = models.CharField(max_length=128, null=True, verbose_name='E-mail')
    subject = models.CharField(max_length=128, verbose_name='Temat')
    message = models.TextField(verbose_name='Wiadomość')
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.subject}, {self.date_sent}'

class Valuation(models.Model):
    first_name = models.CharField(max_length=128, verbose_name="Podaj Imię:")
    last_name = models.CharField(max_length=128, verbose_name="Nazwisko:", null=True)
    mail = models.CharField(max_length=128,verbose_name="E-mail:")
    phone = models.IntegerField(verbose_name="Telefon:")
    TOPIC = (
        (0, '------'),
        (1, "klimatyzacje"),
        (2, "ozonowanie"),
        (3, "pompy ciepła"),
    )
    topic = models.IntegerField(choices=TOPIC, verbose_name="Temat:")
    area = models.IntegerField(verbose_name="Metraż w m2:", null=True)
    cubature = models.IntegerField(verbose_name="Kubatura w m3:", null=True)
    BULDING =(
        (0, '-----'),
        (1, "Dom jednorodzinny"),
        (2, "Mieszkanie w bloku"),
        (3, "Biuro"),
        (4, "Hala magazynowa/produkcyjna"),
    )
    bulding = models.IntegerField(choices=BULDING, verbose_name="Typ budynku:", null=True)
    FLOR = (
        (0, '-----'),
        (1, "parter"),
        (2, "1 piętro"),
        (3, "2 piętro"),
        (4, "3 piętro"),
        (5, "4 piętro"),
        (6, "5 piętro"),
        (7, "wysokie piętro - powyżej 5 pięra")
    )
    flor = models.IntegerField(choices=FLOR, verbose_name="Ilość pięter:", null=True)
    message = models.TextField(verbose_name="Uwagi:")
    date_sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.first_name}, {self.topic}, {self.date_sent}'

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products=models.ManyToManyField(AirProduct)

from django.contrib.auth.signals import user_logged_in

def create_profil(sender, user,request, **kwargs):
    Profil.objects.get_or_create(user=user)

user_logged_in.connect(create_profil)



class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(AirProduct, through="OrderProduct")

    def __str__(self):
        return self.user.username

class OrderProduct(models.Model):
    products = models.ForeignKey(AirProduct, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.products.name


class Cart(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(AirProduct, through="CartProducts")

    def __str__(self):
        return self.client.name


class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(AirProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.quantity == 0:
            self.delete()
        else:
            super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name

