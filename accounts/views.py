from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets
from .forms import DoctorRegistrationForm
from .models import Doctor, Session
from .forms import BookingForm
from .utils import search_doctors
from .serializers import DoctorSerializer, PatientSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.http import JsonResponse


def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Doctor registered successfully'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


class PatientRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


#class DoctorRegistrationAPIView(APIView):
 #   def get(self, request, *args, **kwargs):
  #      doctors = Doctor.objects.all()
    #    serializer = DoctorSerializer(doctors, many=True)
     #   return Response(serializer.data, status=status.HTTP_200_OK)

    #def post(self, request, *args, **kwargs):
     #   form = DoctorRegistrationForm(request.POST, request.FILES)
      #  if form.is_valid():
       #     doctor = form.save()
        #    serializer = DoctorSerializer(doctor)
         #   return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)