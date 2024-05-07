from django.contrib import admin
from django.urls import path
from store.Views.login import LoginView
from store.Views.tech_form import AddPatient, LogoutView, UploadView, patient_id_list, Audiometry, Optometry, Vitals
from store.Views.dashboard import Dashboard
from store.Views.UpdatePatient import UpdatePatient, DeletePatient



urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('dashboard', Dashboard.as_view(), name="dashboard"),
    path('form', AddPatient.as_view(), name="form"),
    path('update_patient/<int:customer_id>/', UpdatePatient.as_view(), name='update_patient'),
    path('delete_patient/<int:customer_id>/', DeletePatient.as_view(), name='delete_patient'),
    path('upload', UploadView.as_view(), name='upload'),
    path('audiometry',Audiometry.as_view(), name = 'audiometry'),
    path('optometry', Optometry.as_view(), name='optometry'),
    path('vitals', Vitals.as_view(), name='vitals'),
    path('vitals1', Vitals.as_view(), name='vitals1'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/patient-ids/', patient_id_list, name='api_patient_ids'),

]
