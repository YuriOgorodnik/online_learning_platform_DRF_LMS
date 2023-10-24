from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


User = get_user_model()


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.all()
        else:
            return User.objects.none()

    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj:
            # Исключаем пароль, фамилию и историю платежей при просмотре профиля другого пользователя
            obj.password = None
            obj.last_name = None
            obj.payment_history = None
        return obj
