from .models import Doctor


def search_doctors(name=None, location=None, specialization=None):
    doctors = Doctor.objects.all()

    if name:
        doctors = doctors.filter(name__icontains=name)

    if location:
        doctors = doctors.filter(location=location)

    if specialization:
        doctors = doctors.filter(specialization=specialization)

    return doctors
