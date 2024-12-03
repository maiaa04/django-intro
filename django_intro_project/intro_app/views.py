from rest_framework import viewsets
from .serializers import ProductSerializer
from .serializers import CustomerSerializer
from .serializers import OrderSerializer
from .models import Product
from .models import Customer
from .models import Order
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .forms import ProductForm

# Create your views here.
from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("Hello, World!")


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    success_url = '../../products/'

    def form_valid(self, form):
        return super().form_valid(form)