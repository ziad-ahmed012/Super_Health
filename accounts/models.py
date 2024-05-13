from datetime import time
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

default_value = timezone.now()
Location_Choices = [('Cairo', 'Cairo'),
                    ('Giza', 'Giza'),
                    ('Alexandria', 'Alexandria'),
                    ]


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, verbose_name="user", on_delete=models.CASCADE)
    name = models.CharField("Name: ", max_length=50)
    email = models.EmailField()
    who_i = models.TextField("Who_i: ", max_length=250)
    price = models.IntegerField("Price: ", blank=False, null=False)
    phone_number = models.CharField(max_length=20)
    doctor_id_image = models.ImageField(upload_to='doctor_ids')
    doctor_image = models.ImageField(upload_to='doctor_images', default='default_image.jpg')
    START_TIME_CHOICES = [
                             (time(hour, 0), f'{hour}:00 AM') for hour in range(0, 12)
                         ] + [
                             (time(hour, 0), f'{hour}:00 PM') for hour in range(1, 12)
                         ]
    END_TIME_CHOICES = [
                           (time(hour, 0), f'{hour}:00 AM') for hour in range(1, 12)
                       ] + [
                           (time(hour, 0), f'{hour}:00 PM') for hour in range(1, 12)
                       ] + [(time(0, 0), '12:00 AM')]  # Add 12:00 AM as the last choice

    start_time = models.TimeField(choices=START_TIME_CHOICES)
    end_time = models.TimeField(choices=END_TIME_CHOICES)
    SPECIALIZATION_CHOICES = [
        ('Cardiologist', 'Cardiologist'),
        ('Dermatologist', 'Dermatologist'),
        ('Endocrinologist', 'Endocrinologist'),
        ('Gastroenterologist', 'Gastroenterologist'),
        ('Neurologist', 'Neurologist'),
        ('Oncologist', 'Oncologist'),
        ('Orthopedic Surgeon', 'Orthopedic Surgeon'),
        ('Pediatrician', 'Pediatrician'),
        ('Psychiatrist', 'Psychiatrist'),
        ('Radiologist', 'Radiologist'),
        ('Urologist', 'Urologist'),
        # Add more choices as needed
    ]
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES, )
    Location = models.CharField(max_length=100, choices=Location_Choices, null=False, default='cairo')

    def __str__(self):
        return self.name


class Patient(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        name = models.CharField(max_length=100)
        email = models.EmailField()
        phone_number = models.CharField(max_length=20)
        Location = models.CharField(max_length=100, choices=Location_Choices, null=False, default='cairo')
        age = models.PositiveIntegerField()
        GENDER_CHOICES = [
            ('M', 'Male'),
            ('F', 'Female'),
        ]
        gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


def __str__(self):
    return self.name


class Session(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(default_value)
    end_datetime = models.DateTimeField(default_value)
