from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'who_i', 'price', 'phone_number',
                  'doctor_image', 'start_time', 'end_time',
                  'specialization', 'Location']
