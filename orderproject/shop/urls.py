from django.urls import path, include 
from .views import RegistrationView, ProtectedView, ProductView, OrderViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r"products", ProductView, basename="products")

urlpatterns = [
    path("api/register/", RegistrationView.as_view(), name="register"),
    path("api/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api/protected/", ProtectedView.as_view(), name="protected"),
    # path('api/', include(router.urls)),
    path("api/products/", ProductView.as_view({"get": "list", "post": "create"}), name="products"),
    path("api/orders/", OrderViewSet.as_view({"get": "list", "post": "create"}), name="orders"),
]