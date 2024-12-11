from django.urls import path
from .views import hello_world
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from .views import CustomerViewSet
from .views import OrderViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')
                
urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
]

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]