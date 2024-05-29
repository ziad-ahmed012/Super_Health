from django.test import TestCase
from django.contrib.auth.models import User
from .forms import DoctorRegistrationForm, PatientRegistrationForm, BookingForm
from accounts.models import Patient, Session
from .models import Doctor
from django.utils import timezone
import datetime


class DoctorRegistrationFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'name': 'Dr. Smith',
            'email': 'dr.smith@example.com',
            'phone_number': '1234567890',
            'doctor_id_image': 'path/to/doctor_id_image.jpg',
            'specialization': 'Cardiology',
            'start_time': '09:00:00',
            'end_time': '17:00:00',
        }
        form = DoctorRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form_data = {
            'name': 'Dr. Smith',
            'email': 'not-an-email',
            'phone_number': '1234567890',
            'doctor_id_image': 'path/to/doctor_id_image.jpg',
            'specialization': 'Cardiology',
            'start_time': '09:00:00',
            'end_time': '17:00:00',
        }
        form = DoctorRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

class PatientRegistrationFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone_number': '0987654321',
            'age': 30,
            'gender': 'M',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        form = PatientRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_email_already_in_use(self):
        User.objects.create_user(username='testuser', email='john.doe@example.com', password='password123')
        form_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone_number': '0987654321',
            'age': 30,
            'gender': 'M',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        form = PatientRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_passwords_do_not_match(self):
        form_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone_number': '0987654321',
            'age': 30,
            'gender': 'M',
            'password': 'password123',
            'confirm_password': 'differentpassword',
        }
        form = PatientRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)

class BookingFormTest(TestCase):

    def test_valid_form(self):
        start_datetime = timezone.now() + datetime.timedelta(days=1)
        end_datetime = start_datetime + datetime.timedelta(hours=1)
        form_data = {
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_end_before_start(self):
        start_datetime = timezone.now() + datetime.timedelta(days=1)
        end_datetime = start_datetime - datetime.timedelta(hours=1)
        form_data = {
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('end_datetime', form.errors)
