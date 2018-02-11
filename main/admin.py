from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    # To show in admin app
    list_display = (
        'staff_id',
        'user',
        'first_name',
        'middle_name',
        'last_name',
        'contact_no',
        'address',
        'email_address',
    )
    # Adding search bar
    search_fields = [
        'staff_id',
        'user',
        'first_name',
        'middle_name',
        'last_name',
        'contact_no',
        'address',
        'email_address',
    ]
    # Categorizing the fields
    fieldsets = (
        (None, {
            'fields': ('profile_picture', ('first_name', 'middle_name', 'last_name'),)
        }),
        ('Contact Information', {
            'fields': (('contact_no', 'email_address'), 'address')
        })
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'customer_id',
        'first_name',
        'middle_name',
        'last_name',
        'contact_no',
        'address',
        'email_address',
    )
    search_fields = [
        'customer_id',
        'first_name',
        'middle_name',
        'last_name',
        'contact_no',
        'address',
        'email_address',
    ]

    fieldsets = (
        (None, {
            'fields': (('first_name', 'middle_name', 'last_name'),)
        }),
        ('Contact Information', {
            'fields': (('contact_no', 'email_address'), 'address')
        })
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'reservation_id',
        'customer',
        'staff',
        'no_of_children',
        'no_of_adults',
        'reservation_date_time',
        'expected_arrival_date_time',
        'expected_departure_date_time',
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_no',
        'room_type',
        'reservation',
        'availability',
        'display_facility',
    )
    # Adding filter
    list_filter = ('room_type', 'availability')
    filter_horizontal = ('facility',)
    fields = (('room_no', 'room_type'), 'reservation', 'facility')
    search_fields = [
        'reservation__customer__first_name',
        'reservation__customer__middle_name',
        'reservation__customer__last_name',
    ]


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
