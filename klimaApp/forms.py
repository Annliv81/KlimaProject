from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import Contact, Producer, Category, Valuation, Order


class AirProductSearchForm(forms.Form):
    name = forms.CharField(label="Nazwa", required=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple,
                                              label="Kategoria")
    producer = forms.ModelMultipleChoiceField(queryset=Producer.objects.all(), widget=forms.CheckboxSelectMultiple,
                                              label="Producent")

    COLORS = (
        (0, '------'),
        (1, "black"),
        (2, "white"),
        (3, "antracyt"),
        (4, "red"),
        (5, "blue")
    )
    color = forms.ChoiceField(choices=COLORS, required=False, label="Kolor")


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=256, label="Nazwa")
    password = forms.CharField(max_length=256, widget=forms.PasswordInput, label="Hasło")


class UserRegisterForm(forms.ModelForm):
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password2',
            'first_name',
            'last_name',
            'email',
        )
        widgets = {
            'password': forms.PasswordInput,
        }

        def clean(self):
            super().clean()

            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise ValidationError('Passwords need to match!')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('date_sent',)

class ValuationForm(forms.ModelForm):
    class Meta:
        model = Valuation
        fields = ('first_name', 'last_name', 'mail', 'phone', 'topic', 'area', 'cubature', 'bulding', 'flor', 'message')
        exclude = ('date_sent',)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('products', 'user')
        exclude = ('date_sent',)