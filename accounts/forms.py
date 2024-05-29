from django import forms
from django.contrib.auth.models import User
from .models import Doctor
from .serializers import DoctorSerializer
from accounts.models import Patient, Session
from django.utils import timezone


default_value = timezone.now()


class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'email', 'phone_number', 'doctor_id_image', 'specialization', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.Select(attrs={'class': 'form-control'}),
            'end_time': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DoctorRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['doctor_id_image'].widget.attrs['class'] = 'form-control-file'
        self.fields['doctor_image'].widget.attrs['class'] = 'form-control-file'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['specialization'].widget.attrs['class'] = 'form-control'


class PatientRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone_number', 'age', 'gender']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different email address.")
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password

    def save(self, commit=True):
        user = super(PatientRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            return user


class BookingForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['start_datetime', 'end_datetime']
