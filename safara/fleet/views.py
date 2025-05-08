from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Driver, Vehicle, FuelLog, TonnageLog, DriverAssignment
from .forms import (
    DriverForm, VehicleForm, FuelLogForm, TonnageLogForm, 
    DriverAssignmentForm, UnassignDriverForm
)

from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class SignUpView(CreateView):
    form_class = UserCreationForm  # Built-in form for username/password
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')  # Redirect to login after signup

# Dashboard view
@login_required
def dashboard(request):
    vehicles = Vehicle.objects.filter(user=request.user)
    active_vehicles = vehicles.filter(status='ACTIVE').count()
    maintenance_vehicles = vehicles.filter(status='MAINTENANCE').count()
    drivers = Driver.objects.filter(user=request.user)
    
    # Get most recent fuel logs
    recent_fuel_logs = FuelLog.objects.filter(
        user=request.user
    ).order_by('-date')[:5]
    
    # Get most recent tonnage logs
    recent_tonnage_logs = TonnageLog.objects.filter(
        user=request.user
    ).order_by('-date')[:5]
    
    context = {
        'total_vehicles': vehicles.count(),
        'active_vehicles': active_vehicles,
        'maintenance_vehicles': maintenance_vehicles,
        'total_drivers': drivers.count(),
        'recent_fuel_logs': recent_fuel_logs,
        'recent_tonnage_logs': recent_tonnage_logs,
    }
    
    return render(request, 'fleet/dashboard.html', context)

# Driver views
@login_required
def driver_list(request):
    drivers = Driver.objects.filter(user=request.user)
    return render(request, 'fleet/driver_list.html', {'drivers': drivers})

@login_required
def driver_detail(request, pk):
    driver = get_object_or_404(Driver, pk=pk, user=request.user)
    # Get current and past vehicle assignments
    current_assignment = DriverAssignment.objects.filter(
        driver=driver, is_active=True
    ).first()
    past_assignments = DriverAssignment.objects.filter(
        driver=driver, is_active=False
    ).order_by('-assigned_at')
    
    context = {
        'driver': driver,
        'current_assignment': current_assignment,
        'past_assignments': past_assignments,
    }
    return render(request, 'fleet/driver_detail.html', context)

@login_required
def driver_create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.user = request.user
            driver.save()
            messages.success(request, 'Driver created successfully')
            return redirect('driver_list')
    else:
        form = DriverForm()
    
    return render(request, 'fleet/driver_form.html', {'form': form})

@login_required
def driver_update(request, pk):
    driver = get_object_or_404(Driver, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver updated successfully')
            return redirect('driver_detail', pk=driver.pk)
    else:
        form = DriverForm(instance=driver)
    
    return render(request, 'fleet/driver_form.html', {'form': form, 'driver': driver})

@login_required
def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk, user=request.user)
    
    if request.method == 'POST':
        driver.delete()
        messages.success(request, 'Driver deleted successfully')
        return redirect('driver_list')
    
    return render(request, 'fleet/driver_confirm_delete.html', {'driver': driver})

# Vehicle views
@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(user=request.user)
    return render(request, 'fleet/vehicle_list.html', {'vehicles': vehicles})

@login_required
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    # Get current driver assignment
    current_assignment = DriverAssignment.objects.filter(
        vehicle=vehicle, is_active=True
    ).first()
    
    # Get fuel logs for this vehicle
    fuel_logs = FuelLog.objects.filter(
        vehicle=vehicle
    ).order_by('-date')[:10]
    
    # Get tonnage logs for this vehicle
    tonnage_logs = TonnageLog.objects.filter(
        vehicle=vehicle
    ).order_by('-date')[:10]
    
    context = {
        'vehicle': vehicle,
        'current_assignment': current_assignment,
        'fuel_logs': fuel_logs,
        'tonnage_logs': tonnage_logs,
    }
    return render(request, 'fleet/vehicle_detail.html', context)

@login_required
def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()
            messages.success(request, 'Vehicle created successfully')
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'fleet/vehicle_form.html', {'form': form})

@login_required
def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully')
            return redirect('vehicle_detail', pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'fleet/vehicle_form.html', {'form': form, 'vehicle': vehicle})

@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully')
        return redirect('vehicle_list')
    
    return render(request, 'fleet/vehicle_confirm_delete.html', {'vehicle': vehicle})

# Driver Assignment views
@login_required
def assign_driver(request):
    if request.method == 'POST':
        form = DriverAssignmentForm(request.POST, user=request.user)
        if form.is_valid():
            vehicle = form.cleaned_data['vehicle']
            driver = form.cleaned_data['driver']
            
            # Use the model method to handle the assignment
            vehicle.assign_driver(driver)
            
            messages.success(request, f'Driver {driver.name} assigned to {vehicle.license_plate}')
            return redirect('vehicle_detail', pk=vehicle.pk)
    else:
        form = DriverAssignmentForm(user=request.user)
    
    return render(request, 'fleet/assign_driver_form.html', {'form': form})

@login_required
def unassign_driver(request, assignment_id):
    assignment = get_object_or_404(
        DriverAssignment, 
        pk=assignment_id, 
        driver__user=request.user,
        is_active=True
    )
    
    if request.method == 'POST':
        form = UnassignDriverForm(request.POST)
        if form.is_valid():
            assignment.unassigned_at = form.cleaned_data['unassignment_date']
            assignment.is_active = False
            assignment.save()
            
            # Update the vehicle's current driver
            vehicle = assignment.vehicle
            vehicle.current_driver = None
            vehicle.save()
            
            messages.success(request, 'Driver unassigned successfully')
            return redirect('vehicle_detail', pk=vehicle.pk)
    else:
        form = UnassignDriverForm(initial={'unassignment_date': timezone.now()})
    
    return render(request, 'fleet/unassign_driver_form.html', {
        'form': form, 
        'assignment': assignment
    })

# Fuel Log views
@login_required
def fuel_log_list(request):
    fuel_logs = FuelLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'fleet/fuel_log_list.html', {'fuel_logs': fuel_logs})

@login_required
def fuel_log_create(request):
    if request.method == 'POST':
        form = FuelLogForm(request.POST, user=request.user)
        if form.is_valid():
            fuel_log = form.save(commit=False)
            fuel_log.user = request.user
            fuel_log.save()
            messages.success(request, 'Fuel log created successfully')
            return redirect('fuel_log_list')
    else:
        form = FuelLogForm(user=request.user)
    
    return render(request, 'fleet/fuel_log_form.html', {'form': form})

@login_required
def fuel_log_update(request, pk):
    fuel_log = get_object_or_404(FuelLog, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = FuelLogForm(request.POST, instance=fuel_log, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fuel log updated successfully')
            return redirect('fuel_log_list')
    else:
        form = FuelLogForm(instance=fuel_log, user=request.user)
    
    return render(request, 'fleet/fuel_log_form.html', {'form': form, 'fuel_log': fuel_log})

@login_required
def fuel_log_delete(request, pk):
    fuel_log = get_object_or_404(FuelLog, pk=pk, user=request.user)
    
    if request.method == 'POST':
        fuel_log.delete()
        messages.success(request, 'Fuel log deleted successfully')
        return redirect('fuel_log_list')
    
    return render(request, 'fleet/fuel_log_confirm_delete.html', {'fuel_log': fuel_log})

# Tonnage Log views
@login_required
def tonnage_log_list(request):
    tonnage_logs = TonnageLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'fleet/tonnage_log_list.html', {'tonnage_logs': tonnage_logs})

@login_required
def tonnage_log_create(request):
    if request.method == 'POST':
        form = TonnageLogForm(request.POST, user=request.user)
        if form.is_valid():
            tonnage_log = form.save(commit=False)
            tonnage_log.user = request.user
            tonnage_log.save()
            messages.success(request, 'Tonnage log created successfully')
            return redirect('tonnage_log_list')
    else:
        form = TonnageLogForm(user=request.user)
    
    return render(request, 'fleet/tonnage_log_form.html', {'form': form})

@login_required
def tonnage_log_update(request, pk):
    tonnage_log = get_object_or_404(TonnageLog, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TonnageLogForm(request.POST, instance=tonnage_log, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tonnage log updated successfully')
            return redirect('tonnage_log_list')
    else:
        form = TonnageLogForm(instance=tonnage_log, user=request.user)
    
    return render(request, 'fleet/tonnage_log_form.html', {'form': form, 'tonnage_log': tonnage_log})

@login_required
def tonnage_log_delete(request, pk):
    tonnage_log = get_object_or_404(TonnageLog, pk=pk, user=request.user)
    
    if request.method == 'POST':
        tonnage_log.delete()
        messages.success(request, 'Tonnage log deleted successfully')
        return redirect('tonnage_log_list')
    
    return render(request, 'fleet/tonnage_log_confirm_delete.html', {'tonnage_log': tonnage_log})