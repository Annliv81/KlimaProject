from django.db import models


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
    name = models.CharField(max_length=128)
    color=models.IntegerField(choices=COLORS, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, null=True, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='klima_image', height_field=None, width_field=None, max_length=100, null=True)
    #biblioteka  pip install Pillow

    def __str__(self):
        return self.name

class Contact(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.subject}, {self.date_sent}'

