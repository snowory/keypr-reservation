from rest_framework import viewsets

from reservation.api.filters import ReservationFilter
from reservation.api.permissions import IsAuthenticatedOrRetrieve
from reservation.api.serializers import ReservationSerializer
from reservation.models import Reservation


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    filter_class = ReservationFilter
    permission_classes = (IsAuthenticatedOrRetrieve,)
