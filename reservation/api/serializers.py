from rest_framework import serializers

from reservation.api.validators import validate_date_period

from reservation.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    def validate(self, data):
        start_date = data['start_date']
        end_date = data['end_date']
        room_number = data['room_number']

        validate_date_period(room_number, start_date, end_date)

        return data


    class Meta:
        model = Reservation
        fields = '__all__'
