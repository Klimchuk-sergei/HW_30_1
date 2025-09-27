from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apps import UsersConfig
from .views import PaymentViewSet, UserRegistrationAPIView, UserViewSet
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "login/",
        TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer),
        name="login",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
]
