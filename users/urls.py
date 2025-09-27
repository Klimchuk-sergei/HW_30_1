from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apps import UsersConfig
from .views import PaymentViewSet, UserRegistrationAPIView, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="login"),  # Убрали кастомный сериализатор
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("profile/", UserViewSet.as_view({'get': 'profile'}), name="profile"),
]