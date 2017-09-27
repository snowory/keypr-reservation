from rest_framework import filters

from reservation.models import Reservation


class ReservationFilter(filters.FilterSet):
    class Meta:
        model = Reservation
        fields = {
            'start_date': ['lte', 'gte', 'gt', 'lt'],
            'end_date': ['lte', 'gte', 'gt', 'lt'],
        }
