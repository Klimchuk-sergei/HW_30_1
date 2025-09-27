from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer, UserCreateSerializer
from .filters import PaymentFilter
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwnerOrStaff


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User Registered Successfully. Now perform Login to get your token.",
            },
            status=status.HTTP_201_CREATED,
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):

        if self.action == "create":
            self.permission_classes = [AllowAny]
        elif self.action in ["retrieve", "update", "partial_update"]:
            # Пользователь может просматривать/редактировать свой профиль, стафф - любой
            self.permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action == "destroy":
            # Только стафф может удалять пользователей
            self.permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action == "list":
            self.permission_classes = [
                IsAuthenticated
            ]  # Список пользователей доступен только авторизованным
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter

    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
