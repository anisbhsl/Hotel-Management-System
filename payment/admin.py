from django.contrib import admin

from .models import CheckIn, CheckOut


# Register your models here.

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'reservation',
        'rooms',
        'initial_amount',
        'check_in_date_time',
        'last_edited_on',
        'user'
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(CheckOut)
class CheckOutAdmin(admin.ModelAdmin):
    list_display = [
        'check_in',
        'stay_duration',
        'total_amount',
        'pay_amount',
        'check_out_date_time',
        'user'
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
