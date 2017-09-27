from django.db import models


class Reservation(models.Model):
    room_number = models.IntegerField()
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField()
