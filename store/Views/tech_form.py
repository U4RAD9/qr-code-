from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
from store.models.customer import Users
from store.models.location import Location
from django.contrib.auth import logout
import pandas as pd
from datetime import datetime  
from .login import user_type_required
from django.http import JsonResponse
import random
from django.db.models import F


# @user_type_required('technician')
class AddPatient(View):
    def get(self, request):
        customers = Users.objects.order_by('-id')
        location = Location.objects.all()
        return render(request, 'form.html', {'customers': customers, 'locations': location})

    def post(self, request):
        if 'submit' in request.POST:
            return self.add_patient(request)
        elif 'save_modalities' in request.POST:
            return self.save_modalities(request)
        else:
            return render(request, 'form.html')

    def add_patient(self, request):
        def random_id():
            patient_random_id = random.randint(100, 10000000)
            id = 'XRAI' + str(patient_random_id)
            return id
        xrai_id = random_id()
        while Users.objects.filter(xrai_id= xrai_id).exists():
            random_id()
        patient_id = request.POST.get('patient_id')
        patient_name = request.POST.get('patient_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        location_id = request.POST.get('location-select')
        date_field = request.POST.get('date-select')
        datetime_obj = datetime.strptime(date_field, "%Y-%m-%d")
        formatted_date = datetime_obj.strftime("%Y-%m-%d")


        try:
            location_instance = Location.objects.get(pk=location_id)
        except Location.DoesNotExist:
            print("Location not found in the database.")
            return HttpResponse("Location not found", status=400)

        # Fetching Data If validation is wrong.
        value = {"patient_id": patient_id,
                 "patient_name": patient_name,
                 "age": age,
                 "gender": gender,
                 "phone": phone,
                 "email": email,
                 "location": location_id,
                 "date": formatted_date}

        # Validate the customer object
        error_message = self.validate_customer(patient_name, age, phone, email)
        if error_message:
            customers = Users.objects.order_by('-id')  # Reverse order by id
            locations = Location.objects.all()
            data = {"error": error_message, "customers": customers, "values": value, "locations": locations}
            return render(request, 'form.html', data)

        if not error_message:
            # Assuming Users is your model for storing patient details
            new_patient = Users.objects.create(
                location=location_instance,
                patient_id=patient_id,
                xrai_id = xrai_id,
                patient_name=patient_name,
                age=age,
                gender=gender,
                phone=phone,
                email=email,
                date_field=formatted_date,
            )

            new_patient.save()
            return redirect('form')
    def validate_customer(self, patient_name, age, phone, email):
        if not patient_name:
            return "Patient Name is required!"
        elif len(patient_name) < 4:
            return "Patient Name must be 4 characters long or more"
        elif len(age) > 120:
            return "Age must between 0-120yrs"
        elif len(phone) < 10 and len(phone) > 10:
            return "Phone Number must be 10 digits"
        elif "@" not in email:
            return "This is not a valid Email"

        return None

    def save_modalities(self, request):
        patient_ids = []
        modality_updates = {}

        for key in request.POST.keys():
            if any(key.startswith(modality) for modality in [
                'registration+', 'xray+', 'ecg+', 'pft+', 'audiometry+',
                'optometry+', 'vitals+', 'pathology+', 'drconsultation+'
            ]):
                patient_id_from_checkbox = key.split('+')[-1]
                patient_ids.append(patient_id_from_checkbox)

                modality_updates[patient_id_from_checkbox] = {
                    'registration': F('registration' if 'registration+{}'.format(patient_id_from_checkbox) in request.POST else False),
                    'xray': F('xray' if 'xray+{}'.format(patient_id_from_checkbox) in request.POST else False),
                    'ecg': F('ecg' if 'ecg+{}'.format(patient_id_from_checkbox) in request.POST else False),
                    'pft': F('pft' if 'pft+{}'.format(patient_id_from_checkbox) in request.POST else False),
                    'audiometry': F('audiometry' if 'audiometry+{}'.format(patient_id_from_checkbox) in request.POST else False),
                    'optometry': F('optometry' if 'optometry+{}'.format(patient_id_from_checkbox) in request.POST else False),
                    'vitals': F('vitals' if 'vitals+{}'.format(patient_id_from_checkbox) in request.POST else False),
                    'pathology': F('pathology' if 'pathology+{}'.format(patient_id_from_checkbox) in request.POST else False),
                    'drconsultation': F('drconsultation' if 'drconsultation+{}'.format(patient_id_from_checkbox) in request.POST else False),
                }

        if patient_ids:
            valid_patient_ids = [pid for pid in patient_ids if pid]
            if valid_patient_ids:
                Users.objects.filter(pk__in=valid_patient_ids).update(**modality_updates)
            else:
                print("No valid patient IDs found in request data")

        return redirect('form')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class UploadView(View):
    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request, *args, **kwargs):
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']

            # Check if the file is an Excel file
            if not excel_file.name.endswith('.xls') and not excel_file.name.endswith('.xlsx'):
                # Handle invalid file format
                return render(request, 'upload.html', {'error': 'Invalid file format'})

            try:
                df = pd.read_excel(excel_file)

                # Iterate through the DataFrame and save data to the Users table
                for index, row in df.iterrows():
                    patient_id = row['patient_id']

                    # Get or create patient by patient_id
                    patient, created = Users.objects.get_or_create(patient_id=patient_id)
                    # Assign values to fields
                    patient.patient_name = row['patient_name']
                    patient.age = row['age']
                    patient.gender = row['gender']
                    patient.location = row['location']
                    patient.phone = row['phone']
                    patient.email = row['email']
                    patient.date_field = row['date_field']
                    patient.audiometry = row['audiometry']
                    patient.ecg = row['ecg']
                    patient.optometry = row['optometry']
                    patient.pft = row['pft']
                    patient.sample_collection = row['drconsultation']
                    patient.vitals = row['vitals']
                    patient.xray = row['xray']
                    patient.registration = row['registration']
                    patient.pathology = row['pathology']

                    patient.save()
                return redirect('dashboard')

            except pd.errors.EmptyDataError:
                return render(request, 'upload.html', {'error': 'Empty Excel file'})

            except Exception as e:
                # Handle other exceptions
                print(f'Error processing Excel file: {e}')
                return render(request, 'upload.html', {'error': f'Error processing Excel file: {e}'})

        return render(request, 'upload.html')

def patient_id_list(request):
    patient_ids = Users.objects.values_list('patient_id', flat=True)
    return JsonResponse(list(patient_ids), safe=False)

class Audiometry(View):
    def get(self, request):
        return redirect('https://docs.google.com/forms/d/1_TV8Z0OpxpjhIvJi2iz1Ke3oru-hS2yqzo9js-E-y5c/viewform?edit_requested=true')

class Optometry(View):
    def get(self, request):
        return redirect('https://docs.google.com/forms/d/1-H8GiIPu5QrbTvSatTYCR0P7sE4WPtZHc__kVw1eb9I/viewform?edit_requested=true')

class Vitals(View):
    def get(self, request):
        return redirect('https://docs.google.com/forms/d/e/1FAIpQLScF3xaTt7VxC4P6sl0ZUShp9E7PVxgXfxN2oV6g0-sCUzmsBQ/viewform')


class Vitals1(View):
    def get(self, request):
        return redirect('https://docs.google.com/forms/d/e/1FAIpQLScQk_GxHRx1WhcM8jOuUsYYOZUA92FbQ6Xr6dblShoxXu8QHQ/viewform')
