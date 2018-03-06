from math import ceil

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.http import HttpRequest

from main.models import Reservation, Room


# Create your models here.
@python_2_unicode_compatible
class CheckIn(models.Model):
    id = models.CharField(max_length=50, primary_key=True, blank=True, editable=False)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    rooms = models.CharField(max_length=50, editable=False, blank=True)
    initial_amount = models.PositiveSmallIntegerField(blank=True, editable=False)
    check_in_date_time = models.DateTimeField(default=timezone.now, editable=False)
    last_edited_on = models.DateTimeField(default=timezone.now, editable=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, editable=False)

    def __str__(self):
        return "%i - %s" % (self.reservation.reservation_id, self.reservation.customer)

    def get_absolute_url(self):
        return reverse('check_in-detail', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.id:
            self.check_in_date_time = timezone.now()
            self.id = "checkin_" + str(self.reservation.reservation_id)
            self.rooms = ', '.join(room.room_no for room in self.reservation.room_set.all())
            self.initial_amount = 0
            for room in self.reservation.room_set.all():
                self.initial_amount += room.room_type.price
                for facility in room.facility.all():
                    self.initial_amount += facility.price
        else:
            reservation = get_object_or_404(CheckIn, id=self.id).reservation
            if self.reservation != reservation:
                self.reservation = reservation

        self.last_edited_on = timezone.now()
        super().save(*args, **kwargs)


@python_2_unicode_compatible
class CheckOut(models.Model):
    check_in = models.OneToOneField(CheckIn, on_delete=models.CASCADE)
    stay_duration = models.DurationField(null=True, editable=False)
    total_amount = models.PositiveSmallIntegerField(default=0, editable=False)
    pay_amount = models.PositiveSmallIntegerField(default=0, editable=False)
    check_out_date_time = models.DateTimeField(editable=False, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            self.check_out_date_time = timezone.now()
            self.stay_duration = self.check_out_date_time - self.check_in.check_in_date_time
            calculated_duration = timezone.timedelta(days=ceil(self.stay_duration.total_seconds() / 3600 / 24))
            self.total_amount = calculated_duration.days * self.check_in.initial_amount
            self.pay_amount = self.total_amount - self.check_in.initial_amount
        super().save(*args, **kwargs)
