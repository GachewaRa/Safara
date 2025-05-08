from datetime import timezone
from django.db import models
from django.contrib.auth.models import User


class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Owner who registered this driver
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name

class DriverAssignment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    unassigned_at = models.DateTimeField(null=True, blank=True)  # Null if still active
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Auto-set is_active based on unassigned_at
        if self.unassigned_at is not None:
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.driver} -> {self.vehicle} ({'Active' if self.is_active else 'Inactive'})"



class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
        ('CAR', 'Car'),
    ]
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('MAINTENANCE', 'In Maintenance'),
        ('RETIRED', 'Retired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to owner
    license_plate = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    current_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_vehicle')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='ACTIVE')

    def assign_driver(self, driver):
        # End any existing active assignment for this vehicle
        DriverAssignment.objects.filter(vehicle=self, is_active=True).update(
            unassigned_at=timezone.now(),
            is_active=False
        )
        # Create new assignment
        self.current_driver = driver
        self.save()
        DriverAssignment.objects.create(driver=driver, vehicle=self)

    def __str__(self):
        return f"{self.license_plate} ({self.vehicle_type})"

class FuelLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateField()
    fuel_amount = models.DecimalField(max_digits=10, decimal_places=2)  # liters/gallons
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    odometer = models.PositiveIntegerField()  # km/miles

    def __str__(self):
        return f"Fuel for {self.vehicle} on {self.date}"

class TonnageLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateField()
    tonnage = models.DecimalField(max_digits=10, decimal_places=2)  # kg/lbs
    origin = models.CharField(max_length=100, blank=True)
    destination = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.tonnage} kg by {self.vehicle} on {self.date}"
