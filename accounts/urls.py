from django.urls import path
from .views import register_doctor, PatientRegistrationAPIView
app_name = 'accounts'
urlpatterns={
path('api/register-doctor/', register_doctor, name='register-doctor'),
path('api/register-patient/', PatientRegistrationAPIView.as_view(), name='register-patient'),
}