from django.urls import path
from .views import register_doctor
app_name = 'accounts'
urlpatterns={
path('api/register-doctor/', register_doctor, name='register-doctor'),
}