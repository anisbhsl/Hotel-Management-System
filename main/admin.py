from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        'staff_id',
        'first_name',
        'last_name',
        'contact_no',
        'address',
        'email_address',
    )
    search_fields = [
        'staff_id',
        'first_name',
        'last_name',
        'contact_no',
        'address',
        'email_address',
    ]

    fieldsets = (
        (None, {
            'fields': ('staff_id', ('first_name', 'last_name'),)
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
        'last_name',
        'contact_no',
        'address',
        'email_address',
    )
    search_fields = [
        'customer_id',
        'first_name',
        'last_name',
        'contact_no',
        'address',
        'email_address',
    ]

    fieldsets = (
        (None, {
            'fields': (('first_name', 'last_name'),)
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
        # 'customer',
        # 'staff'
    )
    list_filter = ('room_type', 'availability')
    fields = (('room_no', 'room_type'), 'reservation')
    search_fields = [
        'reservation__customer__first_name',
        'reservation__customer__last_name',
    ]
