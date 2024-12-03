from django.urls import path
from .views import hello_world
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from .views import CustomerViewSet
from .views import OrderViewSet
from .views import ProductListView, ProductDetailView, ProductCreateView


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')
                
urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
]
urlpatterns = [
    path('api/', include(router.urls)),
    path('user/products/', ProductListView.as_view(), name='product_list'),
    path('user/products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('user/products/new/', ProductCreateView.as_view(), name='product_create'),
]