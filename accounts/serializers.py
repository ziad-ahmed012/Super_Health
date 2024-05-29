from rest_framework import serializers
from .models import Doctor, Patient
from django.contrib.auth.models import User


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'who_i', 'price', 'phone_number', 'doctor_id_image',
                  'doctor_image', 'start_time', 'end_time',
                  'specialization', 'Location']


class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone_number', 'age', 'gender', 'password', 'confirm_password', 'Patient_image']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use. Please use a different email address.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = Patient(**validated_data)
        user.save(validated_data['password'])
        user.save()
        return user
