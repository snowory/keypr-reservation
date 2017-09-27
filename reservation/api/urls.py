from rest_framework.routers import DefaultRouter
from reservation.api.views import ReservationViewSet

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, base_name='reservation')
urlpatterns = router.urls
