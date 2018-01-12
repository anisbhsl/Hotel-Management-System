from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Staff(models.Model):
    """ Model for staffs """
    staff_id = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    email_address = models.EmailField()

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):  # Unicode support
        return '({0}) {1} {2}'.format(self.staff_id, self.first_name, self.last_name)


@python_2_unicode_compatible
class Customer(models.Model):
    """Model for customers"""
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    email_address = models.EmailField(null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('customer-detail', args=str([self.customer_id]))

    def __str__(self):
        return '({0}) {1} {2}'.format(self.customer_id, self.first_name, self.last_name)


@python_2_unicode_compatible
class Reservation(models.Model):
    """Models for reservations"""
    reservation_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='%(class)s_customer')
    staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, related_name='%(class)s_staff')
    no_of_children = models.PositiveSmallIntegerField(default=0)
    no_of_adults = models.PositiveSmallIntegerField(default=1)
    reservation_date_time = models.DateTimeField(default=timezone.now)
    expected_arrival_date_time = models.DateTimeField(default=timezone.now)
    expected_departure_date_time = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('reservation-detail', args=str([self.reservation_id]))

    def __str__(self):
        return '({0}) {1} {2}'.format(self.reservation_id, self.customer.first_name, self.customer.last_name)


@python_2_unicode_compatible
class Room(models.Model):
    SIMPLE = 'SM'
    DELUXE = 'DX'
    PREMIUM = 'PM'
    ROOM_CHOICES = (
        (SIMPLE, 'Simple'),
        (DELUXE, 'Deluxe'),
        (PREMIUM, 'Premium')
    )

    room_no = models.CharField(max_length=10, primary_key=True)
    room_type = models.CharField(max_length=2, choices=ROOM_CHOICES, default=SIMPLE)
    availability = models.BooleanField(default=0)
    reservation = models.ForeignKey(Reservation, null=True, blank=True, on_delete=models.CASCADE)

    # customer = models.ForeignKey(Reservation, null=True, blank=True, on_delete=models.CASCADE,
    #                            related_name='%(class)s_customer')
    # staff = models.ForeignKey(Reservation, null=True, blank=True, on_delete=models.CASCADE,
    #                          related_name='%(class)s_staff')

    class Meta:
        ordering = ['room_no', ]

    def __str__(self):
        return self.room_no

    def get_absolute_url(self):
        return reverse('room-detail', args=[self.room_no])

    def save(self, *args, **kwargs):  # Overriding default behaviour of save
        if self.reservation:  # If it is reserved, than it should not be available
            self.availability = 0
        else:
            self.availability = 1

        super().save(*args, **kwargs)
