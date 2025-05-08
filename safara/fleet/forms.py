from django import forms
from .models import Driver, Vehicle, FuelLog, TonnageLog, DriverAssignment

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license_number', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'vehicle_type', 'make', 'model', 'year', 'status']
        widgets = {
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'make': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class DriverAssignmentForm(forms.ModelForm):
    class Meta:
        model = DriverAssignment
        fields = ['driver', 'vehicle']
        widgets = {
            'driver': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filter queryset to only show this user's drivers and vehicles
            self.fields['driver'].queryset = Driver.objects.filter(user=user)
            self.fields['vehicle'].queryset = Vehicle.objects.filter(user=user)

class UnassignDriverForm(forms.Form):
    unassignment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=True
    )

class FuelLogForm(forms.ModelForm):
    class Meta:
        model = FuelLog
        fields = ['vehicle', 'date', 'fuel_amount', 'cost', 'odometer']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fuel_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'odometer': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Only show this user's vehicles
            self.fields['vehicle'].queryset = Vehicle.objects.filter(user=user)

class TonnageLogForm(forms.ModelForm):
    class Meta:
        model = TonnageLog
        fields = ['vehicle', 'date', 'tonnage', 'origin', 'destination']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tonnage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'origin': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Only show this user's vehicles
            self.fields['vehicle'].queryset = Vehicle.objects.filter(user=user)