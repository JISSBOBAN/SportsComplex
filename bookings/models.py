# booking/models.py

from django.db import models

class Sport(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Booking(models.Model):
    sport_type = models.ForeignKey(Sport, on_delete=models.CASCADE)
    selected_date = models.DateField()
    selected_slot = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sport} - {self.date} - {self.timeslot}"
