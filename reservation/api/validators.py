from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from reservation.models import Reservation


def is_overlap(start1, start2, end1, end2):
    """
    Will return True if at least one of next is True:
        - second range starts within the first range
        - second range ends within the first range
        - second range contains the first range
    """
    return (start1 <= start2 < end1 or
            start1 <= end2 <= end1 or
            start2 <= start1 and end2 >= end1)


def validate_date_period(room_number, start_date, end_date):
    """
    Start date of the reservation cannot be greater than end date of that same
    reservation.
    Start date cannot be equal to end date,
    since cannot make reservation for less than a day.
    """

    if start_date >= end_date:
        raise ValidationError(
            _('Start date cannot be greater or equal than end date.')
        )

    existing_reservations = Reservation.objects.filter(room_number=room_number)

    found = False
    for reservation in existing_reservations:
        if is_overlap(reservation.start_date,
                      start_date,
                      reservation.end_date,
                      end_date):
            found = True
            break

    if found:
        raise ValidationError(
            _('This overlaps with already existing reservation.')
        )
