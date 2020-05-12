from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from .models import AirProduct, Category, Producer, Contact
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, FormView, UpdateView
from .forms import UserLoginForm, AirProductSearchForm, ContactForm, UserRegisterForm
from django.contrib.auth.models import User



# Create your views here.

class UserLoginView(FormView):
    form_class=UserLoginForm
    template_name='klimaApp/form.html'
    success_url ='/'

    def form_valid(self, form):
        user = authenticate(**form.cleaned_data)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)

class UserLogoutView(LogoutView):
    next_page = '/'

class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'klimaApp/form.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        return redirect('/')

class IndexView(View):
    def get(self, request):
        form = ContactForm()
        return render(
            request,
            "klimaApp/o_nas.html", {'form':form}
        )


class ProductListView(View):
    def get(self, request):
        products = AirProduct.objects.order_by("producer__name")
        return render(request,
                      'klimaApp/products.html',
                      {'products': products},
                      )

class ProductDetailsView(View):
    def get(self, request,id):
        product_details = AirProduct.objects.get(id=id)
        return render(
            request,
            'klimaApp/product_details.html',
            {'product_details': product_details}
        )

class AddProductView(PermissionRequiredMixin, CreateView):
    model = AirProduct
    login_url = '/admin'
    fields = ['name', 'color', 'description', 'price', 'category', 'producer', 'foto', 'available']
    template_name = 'klimaApp/add_product.html'
    permission_required = 'klimaApp.add_product'
    success_url = '/oferts'

class ProductEditView(PermissionRequiredMixin,UpdateView):
    model = AirProduct
    template_name = "klimaApp/product_edit.html"
    pk_url_kwarg = "product_id"
    permission_required = "klimaApp.change_product"
    permission_denied_message = "Sorry, You don't have permission"
    fields = ['name', 'color', 'description', 'price', 'category', 'producer', 'foto', 'available']
    success_url = "/oferts/"

"""
from django import forms
class APForm(forms.ModelForm):
    class Meta:
        model = AirProduct
        fields = ['name', 'color', 'description', 'price', 'category', 'producer', 'foto', 'available']

class UpdeteProductView(View):
    def get(self,request,  product_id):
        product = AirProduct.objects.get(pk=product_id)
        form = APForm(instance=product)
        return render(request,"klimaApp/product_edit.html",{'form':form})

    def post(self, request, product_id):
        product = AirProduct.objects.get(pk=product_id)
        form = APForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("/oferts/")
        return render(request, "klimaApp/product_edit.html", {'form': form})

"""
class ProductDeleteView(PermissionRequiredMixin,DeleteView):
    model = AirProduct
    template_name = "klimaApp/product_delete.html"
    pk_url_kwarg = "product_id"
    permission_required = "klimaApp.delete_product"
    permission_denied_message = "Sorry, You don't have permission"
    success_url = '/oferts/'

class ProductSearchView(View):
    def get(self, request):
        products = AirProduct.objects.all()
        form = AirProductSearchForm(request.GET)
        form.is_valid()
        name = form.cleaned_data.get('name')
        if name is not None:
            products = products.filter(name__icontains=name)

        producer = form.cleaned_data.get('producer')
        if producer is not None:
            products = products.filter(producer__in=producer)

        category = form.cleaned_data.get('category')
        if category is not None:
            products = products.filter(category__in=category)

        try:
            color = int(form.cleaned_data.get('color'))
        except:
            color=0
        if color!=0:
            products = products.filter(color=color)

        return render(request, 'klimaApp/product_search.html', {'form': form, 'object_list':products})


class CategoryListView(View):
    def get(self, request):
        categorys = Category.objects.all().order_by('name')
        return render(
            request,
            'klimaApp/categories.html',
            {'categorys': categorys}
        )

class CategorytDetailsView(View):
    def get(self, request,id):
        category_details = Category.objects.get(id=id)
        return render(
            request,
            'klimaApp/category_details.html',
            {'category_details': category_details}
        )
class AddCategoryView(PermissionRequiredMixin, CreateView):
    model = Category
    template_name = "klimaApp/add_category.html"
    permission_required = "klimaApp.add_category"
    permission_denied_message = "Sorry, You don't have permission"
    fields = ["name"]
    success_url = "/categories/"

class CategoryEditView(PermissionRequiredMixin,UpdateView):
    model = Category
    template_name = "klimaApp/form.html"
    pk_url_kwarg = "category_id"
    permission_required = "klimaApp.change_category"
    permission_denied_message = "Sorry, You don't have permission"
    fields = ['name']
    success_url = "/categories/"

class CategoryDeleteView(PermissionRequiredMixin,DeleteView):
    model = Category
    template_name = "klimaApp/product_delete.html"
    pk_url_kwarg = "category_id"
    permission_required = "klimaApp.delete_category"
    permission_denied_message = "Sorry, You don't have permission"
    success_url = '/categories/'

class ProducerListView(View):
    def get(self, request):
        producers = Producer.objects.all().order_by('name')
        return render(
            request,
            'klimaApp/producers.html',
            {'producers': producers}
        )


class AddProducerView(PermissionRequiredMixin, CreateView):
    model = Producer
    template_name = "klimaApp/add_producer.html"
    permission_required = "klimaApp.add_producer"
    permission_denied_message = "Sorry, You don't have permission"
    fields = ["name"]
    success_url = "/producers/"

class ProducerEditView(PermissionRequiredMixin,UpdateView):
    model = Producer
    template_name = "klimaApp/form.html"
    pk_url_kwarg = "producer_id"
    permission_required = "klimaApp.change_producer"
    permission_denied_message = "Sorry, You don't have permission"
    fields = ['name']
    success_url = "/producers/"

class ProducerDeleteView(PermissionRequiredMixin,DeleteView):
    model = Producer
    template_name = "klimaApp/product_delete.html"
    pk_url_kwarg = "producer_id"
    permission_required = "klimaApp.delete_producer"
    permission_denied_message = "Sorry, You don't have permission"
    success_url = '/producers/'

class MontazView(View):
    def get(self, request):
        return render(
            request,
            'klimaApp/montaz.html',
        )

class CertyfikatView(View):
    def get(self, request):
        return render(
            request,
            'klimaApp/certyfikaty.html',
        )

class ContactFormView(CreateView):
    form_class = ContactForm
    template_name = 'klimaApp/kontakt.html'
    success_url = '/kontakt/'

class MessageListView(ListView):
    queryset = Contact.objects.all()
    template_name = 'klimaApp/list.html'
"""
class AddItemToCardView(View):
    def get(self, request, id_product):
        cart, created=Cart.objects.get_or_create(user=request.user)
        air = AirProduct.objects.get(id=id_product)
        cart.product.add(air)
        return HttpResponse("dodaliśmy wszytko")

class CartView(View):
    def get(self, request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'klimaApp/shoping_cart.html', {'cart':"cart"})
"""


class OzoneView(View):
    def get(self, request):
        return render(
            request,
            'klimaApp/ozone.html',
        )

class PompView(View):
    def get(self, request):
        return render(
            request,
            'klimaApp/pomps.html',
        )