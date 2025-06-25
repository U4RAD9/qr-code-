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
        return render(request, 'form.html', {'customers': customers, 'locations': location, 'disabled_flags': {}})

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
        for key in request.POST.keys():
            if any(key.startswith(modality) for modality in
                   ['registration+', 'xray+', 'ecg+', 'pft+', 'audiometry+', 'optometry+', 'vitals+', 'pathology+',
                    'drconsultation+']):
                patient_id_from_checkbox = key.split('+')[-1]
                print(patient_id_from_checkbox)

                # Fetch the corresponding patient instances
                patients = Users.objects.filter(patient_id=patient_id_from_checkbox)

                if not patients.exists():
                    return HttpResponse("Patient not found", status=400)

                # Iterate over the queryset of patients
                for patient in patients:
                    # Fetch the current values from the database
                    current_registration = patient.registration
                    current_xray = patient.xray
                    current_ecg = patient.ecg
                    current_pft = patient.pft
                    current_audiometry = patient.audiometry
                    current_optometry = patient.optometry
                    current_vitals = patient.vitals
                    current_pathology = patient.pathology
                    current_drconsultation = patient.drconsultation

                    # Update the modalities based on the form data if the checkbox is checked
                    if 'registration+{}'.format(patient_id_from_checkbox) in request.POST:
                        patient.registration = True
                    if 'xray+{}'.format(patient_id_from_checkbox) in request.POST:
                        patient.xray = True
                    if 'ecg+{}'.format(patient_id_from_checkbox) in request.POST:
                        patient.ecg = True
                    if 'pft+{}'.format(patient_id_from_checkbox) in request.POST:
                        patient.pft = True
                    if 'audiometry+{}'.format(patient_id_from_checkbox) in request.POST:
                        patient.audiometry = True
                    if 'optometry+{}'.format(patient_id_from_checkbox) in request.POST:
                        patient.optometry = True
                    if 'vitals+{}'.format(patient_id_from_checkbox) in request.POST:
                        patient.vitals = True
                    if 'drconsultation+{}'.format(patient_id_from_checkbox) in request.POST:
                        patient.drconsultation = True
                    if 'pathology+{}'.format(patient_id_from_checkbox) in request.POST:
                        patient.pathology = True

                    # If a checkbox was unchecked in the form but is already checked in the database, prevent the update
                    if not patient.registration and current_registration:
                        patient.registration = current_registration
                    if not patient.xray and current_xray:
                        patient.xray = current_xray
                    if not patient.ecg and current_ecg:
                        patient.ecg = current_ecg
                    if not patient.pft and current_pft:
                        patient.pft = current_pft
                    if not patient.audiometry and current_audiometry:
                        patient.audiometry = current_audiometry
                    if not patient.optometry and current_optometry:
                        patient.optometry = current_optometry
                    if not patient.vitals and current_vitals:
                        patient.vitals = current_vitals
                    if not patient.drconsultation and current_drconsultation:
                        patient.drconsultation = current_drconsultation
                    if not patient.pathology and current_pathology:
                        patient.pathology = current_pathology

                    patient.save()

        return redirect('form')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

# class UploadView(View):
#     def get(self, request):
#         return render(request, 'upload.html')

#     def post(self, request, *args, **kwargs):
#         if 'excel_file' in request.FILES:
#             excel_file = request.FILES['excel_file']

#             # Check file extension
#             if not excel_file.name.endswith('.xls') and not excel_file.name.endswith('.xlsx'):
#                 return render(request, 'upload.html', {'error': 'Invalid file format. Please upload .xls or .xlsx file'})

#             try:
#                 # Try importing required dependencies
#                 try:
#                     import openpyxl
#                 except ImportError:
#                     return render(request, 'upload.html', 
#                         {'error': 'Missing openpyxl module. Please contact administrator.'})

#                 df = pd.read_excel(excel_file, engine='openpyxl')

#                 # Verify required columns exist
#                 required_columns = ['patient_id', 'Location']
#                 missing_columns = [col for col in required_columns if col not in df.columns]
#                 if missing_columns:
#                     return render(request, 'upload.html', 
#                         {'error': f'Missing required columns: {", ".join(missing_columns)}'})

#                 # Iterate through the DataFrame and save data to the Users table
#                 for index, row in df.iterrows():
#                     patient_id = row['patient_id']

#                     # Get the location instance based on location name from Excel
#                     try:
#                         location_name = row['Location']
#                         location_instance = Location.objects.get(name=location_name)
#                     except Location.DoesNotExist:
#                         return render(request, 'upload.html', 
#                             {'error': f'Location "{location_name}" not found in database'})
#                     except KeyError:
#                         return render(request, 'upload.html', 
#                             {'error': 'Location column missing in Excel file'})

#                     # Get or create patient by patient_id
#                     patient, created = Users.objects.get_or_create(
#                         patient_id=patient_id,
#                         defaults={'location': location_instance}
#                     )

#                     # Map Excel columns to model fields
#                     field_mapping = {
#                         'patient_name': 'patient_name',
#                         'age': 'age', 
#                         'gender': 'gender',
#                         'phone': 'phone',
#                         'email': 'email',
#                         'date_field': 'date_field',
#                         'audiometry': 'audiometry',
#                         'ecg': 'ecg',
#                         'optometry': 'optometry',
#                         'pft': 'pft',
#                         'drconsultation': 'drconsultation',
#                         'vitals': 'vitals',
#                         'xray': 'xray',
#                         'registration': 'registration',
#                         'pathology': 'pathology'
#                     }

#                     # Update patient fields from Excel
#                     for excel_col, model_field in field_mapping.items():
#                         if excel_col in row:
#                             value = row[excel_col]
#                             # Convert date string to datetime if needed
#                             if model_field == 'date_field' and isinstance(value, str):
#                                 try:
#                                     value = datetime.strptime(value, '%Y-%m-%d').date()
#                                 except ValueError:
#                                     continue
#                             setattr(patient, model_field, value)

#                     # Update location
#                     patient.location = location_instance
#                     patient.save()

#                 return redirect('dashboard')

#             except pd.errors.EmptyDataError:
#                 return render(request, 'upload.html', {'error': 'The Excel file is empty'})
#             except Exception as e:
#                 print(f'Error processing Excel file: {str(e)}')
#                 return render(request, 'upload.html', 
#                     {'error': f'Error processing Excel file: {str(e)}'})

#         return render(request, 'upload.html')


class UploadView(View):
    def get(self, request):
        disabled_flags = request.session.get('disabled_flags', {})
        customers = Users.objects.all()
        locations = Location.objects.all()
        return render(request, 'upload.html', {
            'disabled_flags': disabled_flags,
            'customers': customers,
            'locations': locations
        })

    def post(self, request, *args, **kwargs):
        if 'excel_file' not in request.FILES:
            return render(request, 'upload.html', {'error': 'No file uploaded'})

        excel_file = request.FILES['excel_file']

        if not excel_file.name.endswith(('.xls', '.xlsx')):
            return render(request, 'upload.html', {
                'error': 'Invalid file format. Please upload .xls or .xlsx file'
            })

        try:
            import openpyxl
        except ImportError:
            return render(request, 'upload.html', {
                'error': 'Missing openpyxl module. Please contact administrator.'
            })

        try:
            df = pd.read_excel(excel_file, engine='openpyxl')
        except pd.errors.EmptyDataError:
            return render(request, 'upload.html', {'error': 'The Excel file is empty'})
        except Exception as e:
            return render(request, 'upload.html', {'error': f'Error reading Excel: {str(e)}'})

        required_columns = ['patient_id', 'Location']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return render(request, 'upload.html', {
                'error': f'Missing required columns: {", ".join(missing_columns)}'
            })

        for index, row in df.iterrows():
            patient_id = row['patient_id']
            try:
                location_instance = Location.objects.get(name=row['Location'])
            except Location.DoesNotExist:
                return render(request, 'upload.html', {
                    'error': f'Location "{row["Location"]}" not found in database'
                })

            patient, created = Users.objects.get_or_create(
                patient_id=patient_id,
                defaults={'location': location_instance}
            )

            # Regular fields
            field_mapping = {
                'patient_name': 'patient_name',
                'age': 'age',
                'gender': 'gender',
                'phone': 'phone',
                'email': 'email',
                'date_field': 'date_field',
            }

            for excel_col, model_field in field_mapping.items():
                if excel_col in row and pd.notna(row[excel_col]):
                    value = row[excel_col]
                    if model_field == 'date_field' and isinstance(value, str):
                        try:
                            value = datetime.strptime(value, '%Y-%m-%d').date()
                        except ValueError:
                            continue
                    setattr(patient, model_field, value)

            # Modality fields
            bool_fields = [
                'audiometry', 'ecg', 'optometry', 'pft',
                'drconsultation', 'vitals', 'xray',
                'registration', 'pathology'
            ]

            for field in bool_fields:
                raw_value = row.get(field)

                # Check if value is NaN or string 'NA'
                if pd.isna(raw_value) or str(raw_value).strip().upper() == 'NA':
                    setattr(patient, field, False)
                    setattr(patient, f"{field}_disabled", True)
                else:
                    is_checked = str(raw_value).strip() == '1'
                    setattr(patient, field, is_checked)
                    setattr(patient, f"{field}_disabled", False)

            patient.location = location_instance
            patient.save()

        return redirect('upload')


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
