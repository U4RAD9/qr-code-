from django.shortcuts import render
from django.views import View
from store.models.customer import Users
from store.models.location import Location
from .login import user_type_required

# @user_type_required('coordinator')
class Dashboard(View):
    def get(self, request):
        email = request.session.get('email')
        password = request.session.get('password')
        customers = Users.objects.order_by('-id')
        location = Location.objects.all()
        unique_dates = set()
        for date in customers:
                unique_dates.add(date.date_field)
        sorted_unique_dates = sorted(unique_dates, reverse=False)
        formatted_dates = [date.strftime('%Y-%m-%d') for date in sorted_unique_dates]
        total_patients_count = Users.objects.count()
        
        selected_location_id = request.GET.get('location', None)
        # print(selected_location_id)
        modalities_filter = {}
        if selected_location_id and selected_location_id != 'all':
                modalities_filter['location_id'] = selected_location_id

        count_modalities = {
            'registration': Users.objects.filter(registration=True, **modalities_filter).count(),
            'xray': Users.objects.filter(xray=True, **modalities_filter).count(),
            'ecg': Users.objects.filter(ecg=True, **modalities_filter).count(),
            'pft': Users.objects.filter(pft=True, **modalities_filter).count(),
            'audiometry': Users.objects.filter(audiometry=True, **modalities_filter).count(),
            'optometry': Users.objects.filter(optometry=True, **modalities_filter).count(),
            'vitals': Users.objects.filter(vitals=True, **modalities_filter).count(),
            'sputum': Users.objects.filter(sputum=True, **modalities_filter).count(),
            'drconsultation': Users.objects.filter(drconsultation=True, **modalities_filter).count(),
            'pathology': Users.objects.filter(pathology=True, **modalities_filter).count(),
        }

        data = {
                'customers': customers,
                'total_patient_counts': total_patients_count,
                'count': count_modalities,
                'locations': location,
                'date': formatted_dates
        }

        return render(request, 'dashboard.html', {'data': data})

        if selected_location_id==1:
                registration = Users.objects.filter(location_id=1, registration=True).count()
                xray_modalities = Users.objects.filter(location_id=1, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=1, ecg=True).count()
                pft_modalities = Users.objects.filter(location_id=1, pft=True).count()
                audiometry_modalities = Users.objects.filter(location_id=1, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=1, optometry=True).count()
                vitals_modalities = Users.objects.filter(location_id=1, vitals=True).count()
                sputum_modalities = Users.objects.filter(location_id=1, sputum=True).count()
                drconsultation_modalities = Users.objects.filter(location_id=1, drconsultation=True).count()
                pathology = Users.objects.filter(location_id=1, sputum=True).count()

        elif selected_location_id==2:
                registration = Users.objects.filter(location_id=2, registration=True).count()
                xray_modalities = Users.objects.filter(location_id=2, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=2, ecg=True).count()
                audiometry_modalities = Users.objects.filter(location_id=2, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=2, optometry=True).count()
                vitals_modalities = Users.objects.filter(location_id=2, vitals=True).count()
                sputum_modalities = Users.objects.filter(location_id=2, sputum=True).count()
                drconsultation_modalities = Users.objects.filter(location_id=2, drconsultation=True).count()
                pathology = Users.objects.filter(location_id=1, sputum=True).count()

        elif selected_location_id==3:
                registration = Users.objects.filter(location_id=3, registration=True).count()
                xray_modalities = Users.objects.filter(location_id=3, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=3, ecg=True).count()
                audiometry_modalities = Users.objects.filter(location_id=3, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=3, optometry=True).count()
                vitals_modalities = Users.objects.filter(location_id=3, vitals=True).count()
                sputum_modalities = Users.objects.filter(location_id=3, sputum=True).count()
                drconsultation_modalities = Users.objects.filter(location_id=3, drconsultation=True).count()
                pathology = Users.objects.filter(location_id=1, sputum=True).count()
        
        elif  selected_location_id==4:
                registration = Users.objects.filter(location_id=4, registration=True).count()
                xray_modalities = Users.objects.filter(location_id=4, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=4, ecg=True).count()
                audiometry_modalities = Users.objects.filter(location_id=4, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=4, optometry=True).count()
                vitals_modalities = Users.objects.filter(location_id=4, vitals=True).count()
                sputum_modalities = Users.objects.filter(location_id=4, sputum=True).count()
                drconsultation_modalities = Users.objects.filter(location_id=4, drconsultation=True).count()
                pathology = Users.objects.filter(location_id=1, sputum=True).count()
        
        else :
                registration = Users.objects.filter(location_id=5, registration=True).count()
                xray_modalities = Users.objects.filter(xray=True).count()
                ecg_modalities = Users.objects.filter(ecg=True).count()
                pft_modalities = Users.objects.filter(pft=True).count()
                audiometry_modalities = Users.objects.filter(audiometry=True).count()
                optometry_modalities = Users.objects.filter(optometry=True).count()
                vitals_modalities = Users.objects.filter(vitals=True).count()
                sputum_modalities = Users.objects.filter(sputum=True).count()
                drconsultation_modalities = Users.objects.filter(drconsultation=True).count()
                pathology = Users.objects.filter(location_id=1, sputum=True).count()

               

        count_modalities = {'xray': xray_modalities,
                            'ecg': ecg_modalities,
                            'pft': pft_modalities,
                            'audiometry': audiometry_modalities,
                            'optometry': optometry_modalities,
                            'vitals': vitals_modalities,
                            'sputum': sputum_modalities,
                            'drconsultation': drconsultation_modalities,
                            'pathology': pathology,
                            'registration': registration}

        data = {'customers': customers, 'total_patient_counts': total_patients_count,
                'count': count_modalities, 'locations': location, 'date': formatted_dates}
        
        return render(request, 'dashboard.html', {'data': data})
   


