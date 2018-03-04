from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Staff(models.Model):
    """ Model for staffs """
    profile_picture = models.ImageField(upload_to='staff_img/', default='images/staff.png')
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=False, blank=True)
    last_name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    email_address = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, editable=False)

    class Meta:
        ordering = ['first_name', 'middle_name', 'last_name']
        permissions = (("can_view_staff", "Can view staff"), ('can_view_staff_detail', 'Can view staff detail'))

    def __str__(self):  # Unicode support
        return '({0}) {1} {2}'.format(self.staff_id, self.first_name, self.last_name)


@python_2_unicode_compatible
class Customer(models.Model):
    """Model for customers"""
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=False, blank=True)
    last_name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    email_address = models.EmailField(null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'middle_name', 'last_name']
        permissions = (('can_view_customer', 'Can view customer'),)

    def get_absolute_url(self):
        """
        This generates the url for customer detail.
        'customer-detail' is the name of the url.
        Takes argument customer_id
        """
        return reverse('customer-detail', args=str([self.customer_id]))

    def __str__(self):
        return '({0}) {1} {2}'.format(self.customer_id, self.first_name, self.last_name)


@python_2_unicode_compatible
class Reservation(models.Model):
    """Models for reservations"""
    reservation_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, editable=False)
    no_of_children = models.PositiveSmallIntegerField(default=0)
    no_of_adults = models.PositiveSmallIntegerField(default=1)
    reservation_date_time = models.DateTimeField(default=timezone.now)
    expected_arrival_date_time = models.DateTimeField(default=timezone.now)
    expected_departure_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        permissions = (('can_view_reservation', 'Can view reservation'),
                       ('can_view_reservation_detail', 'Can view reservation detail'),)

    def get_absolute_url(self):
        return reverse('reservation-detail', args=str([self.reservation_id]))

    def __str__(self):
        return '({0}) {1} {2}'.format(self.reservation_id, self.customer.first_name, self.customer.last_name)


@python_2_unicode_compatible
class Room(models.Model):
    room_no = models.CharField(max_length=10, primary_key=True)
    room_type = models.ForeignKey('RoomType', null=False, blank=True, on_delete=models.CASCADE)
    availability = models.BooleanField(default=0)
    reservation = models.ForeignKey(Reservation, null=True, blank=True, on_delete=models.SET_NULL)
    facility = models.ManyToManyField('Facility')

    class Meta:
        ordering = ['room_no', ]
        permissions = (('can_view_room', 'Can view room'),)

    def __str__(self):
        return "%s - %s - Rs. %i" % (self.room_no, self.room_type.name, self.room_type.price)

    def display_facility(self):
        """
        This function should be defined since facility is many-to-many relationship
        It cannot be displayed directly on the admin panel for list_display
        """
        return ', '.join([facility.name for facility in self.facility.all()])

    display_facility.short_description = 'Facilities'

    def get_absolute_url(self):
        return reverse('room-detail', args=[self.room_no])

    def save(self, *args, **kwargs):  # Overriding default behaviour of save
        if self.reservation:  # If it is reserved, than it should not be available
            self.availability = 0
        else:
            self.availability = 1

        super().save(*args, **kwargs)


@python_2_unicode_compatible
class Facility(models.Model):
    name = models.CharField(max_length=25)
    price = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'Facilities'  # Otherwise admin panel shows Facilitys

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class RoomType(models.Model):
    name = models.CharField(max_length=25)
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

