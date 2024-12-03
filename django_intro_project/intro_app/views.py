from rest_framework import viewsets
from .serializers import ProductSerializer
from .serializers import CustomerSerializer
from .serializers import OrderSerializer
from .models import Product
from .models import Customer
from .models import Order

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
