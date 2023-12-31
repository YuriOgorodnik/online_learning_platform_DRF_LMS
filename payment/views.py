from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentListAPIView(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method")
    ordering_fields = ("date",)
    permission_classes = [IsAuthenticated]
