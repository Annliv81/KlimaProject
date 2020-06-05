from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from .models import AirProduct, Category, Producer, Profil, Order, Cart, CartProducts
from django.views.generic import CreateView, ListView, DeleteView, FormView, UpdateView, DetailView
from .forms import UserLoginForm, AirProductSearchForm, ContactForm, UserRegisterForm, ValuationForm, OrderForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin




# Create your views here.

#### logowanie i rejestracja #############################################################################

class UserLoginView(FormView):
    form_class=UserLoginForm
    template_name='klimaApp/form.html'
    success_url ='/products/'

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
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        Profil.objects.create(user=user)
        return super().form_valid(form)


################# Podstrony html ##########################################################################
############# strona o nas###
class IndexView(View):
    def get(self, request):
        form = ContactForm()
        form2 = ValuationForm()
        return render(
            request,
            "klimaApp/o_nas.html", {'form':form, 'form2':form2}
        )
    """
class MontazView(View):
    def get(self, request):
        form = PricesForm()
        return render(
            request,
            'klimaApp/montaz.html', {'form':form}
        )
"""

class CertyficateView(View):
    def get(self, request):
        return render(
            request,
            'klimaApp/certificate.html',
        )

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

################### PRODUKT ##############################################################################

#produkty wyświetlane za pomogą templatki products.html na stronie /oferts.html
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
    success_url = '/products'

class ProductEditView(PermissionRequiredMixin,UpdateView):
    model = AirProduct
    template_name = "klimaApp/form.html"
    pk_url_kwarg = "product_id"
    permission_required = "klimaApp.change_product"
    permission_denied_message = "Sorry, You don't have permission"
    fields = ['name', 'color', 'description', 'price', 'category', 'producer', 'foto', 'available']
    success_url = "/products/"

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
    success_url = '/products/'

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

###################### CATEGORY - KATEGORIA ####################################################################

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


######################### PRODUCERS - PRODUCENCI ###########################################################

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


##################### WIDOKI OD FORMULARZY ######################

class ContactFormView(CreateView):
    form_class = ContactForm
    template_name = 'klimaApp/contact.html'
    text = 'Wypełnij formularz, skontaktujemy się z Tobą'
    success_url = '/contact/'

class ValuationFormView(CreateView):
    form_class = ValuationForm
    template_name = 'klimaApp/montaz.html'
    success_url = '/montaz/'

class CartView(View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(client=request.user)
        return render(request, 'klimaApp/cart.html', {'cart':cart})


class AddAirProductToCartView(View):
    def get(self, request, id_product):
        cart, created = Cart.objects.get_or_create(client=request.user)
        product = AirProduct.objects.get(id=id_product)
        cart.products.add(product)
        return redirect('/products/')

def cart_details(request):
    cart=Cart.objects.get(client=request.user)
    cart_products= CartProducts.objects.filter(cart=cart)
    return render(request, 'klimaApp/cart.html', {'cart':cart, 'cart_products':cart_products})


class RemoveAirFromCardView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        cart = Cart.objects.get(client=request.user)
        product = AirProduct.objects.get(id=product_id)
        cart.products.remove(product)
        return redirect('cart')

class ChangeQuantity(View):
    def post(self, request, product_id):
        cart = Cart.objects.get(client=request.user)
        product = AirProduct.objects.get(pk=product_id)
        kp = CartProducts.objects.get(cart=cart, product=product)
        if request.POST.get("type")=='+':
            kp.quantity +=1
        elif request.POST.get("type")=="-":
            kp.quantity -=1
        else:
            kp.quantity= 0
        kp.save()
        return redirect(f"/cart/")
class ProfilView(DetailView):
    model = Profil
    template_name = "klimaApp/profil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.request.user.order_set.all()
        return context

class OrderView(View):
    def get(self, request):
        form = OrderForm()
        return render(request, 'klimaApp/order.html', {"form":form})
    def post(self, request):
        order = Order()
        order.user = request.user
        order.save()
        cart = request.user.cart
        order.products.set(cart.products.all())
        cart.products.clear()
        return render(request, "klimaApp/order_confirmation.html", {'order':order})




