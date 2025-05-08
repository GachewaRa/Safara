from django.contrib import admin
from .models import Driver, Vehicle, FuelLog, TonnageLog, DriverAssignment

class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'phone', 'user')
    list_filter = ('user',)
    search_fields = ('name', 'license_number')

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'make', 'model', 'year', 'vehicle_type', 'status', 'user')
    list_filter = ('vehicle_type', 'status', 'user')
    search_fields = ('license_plate', 'make', 'model')

class DriverAssignmentAdmin(admin.ModelAdmin):
    list_display = ('driver', 'vehicle', 'assigned_at', 'unassigned_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('driver__name', 'vehicle__license_plate')
    date_hierarchy = 'assigned_at'

class FuelLogAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date', 'fuel_amount', 'cost', 'odometer', 'user')
    list_filter = ('date', 'user')
    search_fields = ('vehicle__license_plate',)
    date_hierarchy = 'date'

class TonnageLogAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date', 'tonnage', 'origin', 'destination', 'user')
    list_filter = ('date', 'user')
    search_fields = ('vehicle__license_plate', 'origin', 'destination')
    date_hierarchy = 'date'

admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(DriverAssignment, DriverAssignmentAdmin)
admin.site.register(FuelLog, FuelLogAdmin)
admin.site.register(TonnageLog, TonnageLogAdmin)