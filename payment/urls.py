from rest_framework.routers import DefaultRouter

from payment.apps import PaymentConfig
from payment.views import PaymentListAPIView

app_name = PaymentConfig.name

router = DefaultRouter()
router.register(r'payments', PaymentListAPIView, basename='payment')

urlpatterns = [
              ] + router.urls
