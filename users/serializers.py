from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from payment.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True, source="payment_set")

    class Meta:
        model = User
        fields = "__all__"
