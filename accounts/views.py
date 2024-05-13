from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets
from .forms import DoctorRegistrationForm
from .models import Doctor, Session
from .forms import BookingForm
from .utils import search_doctors
from .serializers import DoctorSerializer


def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = DoctorRegistrationForm()
    return render(request, '', {'form': form})


def book_session(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data['start_datetime']
            end_datetime = form.cleaned_data['end_datetime']
            # Check if the requested time slot is available
            if is_slot_available(doctor, start_datetime, end_datetime):
                session = Session(doctor=doctor, patient=request.user.patient, start_datetime=start_datetime, end_datetime=end_datetime)
                session.save()
                messages.success(request, 'Session booked successfully!')
                return redirect('home')  # Redirect to home or another page
            else:
                messages.error(request, 'The requested time slot is not available. Please choose another time.')
    else:
        form = BookingForm()
    return render(request, '', {'form': form, 'doctor': doctor})


def is_slot_available(doctor, start_datetime, end_datetime):
    # Check if any existing session overlaps with the requested time slot
    existing_sessions = Session.objects.filter(doctor=doctor, start_datetime__lt=end_datetime, end_datetime__gt=start_datetime)
    return not existing_sessions.exists()


def search_view(request):
    name = request.GET.get('name')
    location = request.GET.get('location')
    specialization = request.GET.get('specialization')

    doctors = search_doctors(name=name, location=location, specialization=specialization)

    context = {
        'doctors': doctors
    }

    return render(request, '', context)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
