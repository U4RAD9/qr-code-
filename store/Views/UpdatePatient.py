from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models.customer import Users

class UpdatePatient(View):
    def get(self, request, customer_id):
        customer = Users.objects.get(id=customer_id)
        return render(request, 'updatepatient.html', {'customer': customer})

    def post(self, request, customer_id):
        
        # If 'optometry_form' is not present, it's a regular patient update form
        customer = get_object_or_404(Users, pk=customer_id)
        customer.patient_id = request.POST.get('patient_id')
        customer.patient_name = request.POST.get('patient_name')
        customer.age = request.POST.get('age')
        customer.gender = request.POST.get('gender')
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email')
        customer.address = request.POST.get('address')

        customer.save()
        return redirect('form')



# delete Data
class DeletePatient(View):
    def post(self, request, customer_id):
        user = Users.objects.get(pk=customer_id)
        user.delete()
        return redirect('form')
