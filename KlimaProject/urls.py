"""KlimaProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from klimaApp.views import(
    IndexView,
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    ProductListView,
    ProductDetailsView,
    ProductDeleteView,
    ProductSearchView,
    AddProductView,
    CategorytDetailsView,
    AddCategoryView,
    CategoryListView,
    CategoryEditView,
    CategoryDeleteView,
    ProducerListView,
    AddProducerView,
    ProducerEditView,
    ProducerDeleteView,
    MontazView,
    CertyfikatView,
    ContactFormView,
    OzoneView,
    PompView,

)
from klimaApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="onas"),
    path('user_login/', UserLoginView.as_view(), name="user-login"),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user_registration/', UserRegisterView.as_view(), name='registration'),
    path('oferts/', ProductListView.as_view(), name='product-list'),
    path('product_details/<int:id>', ProductDetailsView.as_view(), name='product-details'),
    path('product_edit/<int:product_id>', views.ProductEditView.as_view(), name="product-edit"),
    path('product_delete/<int:product_id>', ProductDeleteView.as_view(), name="product-delete"),
    path('product_search/', ProductSearchView.as_view(), name="product-search"),
    path('product_add/', AddProductView.as_view(), name='product-add'),
    path('category_add/', AddCategoryView.as_view(), name='category-add'),
    path('category_edit/<int:category_id>', CategoryEditView.as_view(), name='category-edit'),
    path('category_delete/<int:category_id>', CategoryDeleteView.as_view(), name='category-delete'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category_details/<int:id>', CategorytDetailsView.as_view(), name='cateogry-details'),
    path('producers/', ProducerListView.as_view(), name="producer-list"),
    path('producer_add/', AddProducerView.as_view(), name='producer-add'),
    path('producer_edit/<int:producer_id>', ProducerEditView.as_view(), name="producer-edit"),
    path('producer_delete/<int:producer_id>', ProducerDeleteView.as_view(), name="producer-delete"),
    path('montaz/', MontazView.as_view(), name='montaz-opis'),
    path('certyfikaty/', CertyfikatView.as_view(), name="certyfikaty"),
    path('kontakt/', ContactFormView.as_view(), name="contact-form"),
    path('ozone/', OzoneView.as_view(), name="ozone"),
    path('pomps/', PompView.as_view(), name="pomps"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)