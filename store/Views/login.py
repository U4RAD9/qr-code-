from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login as ContribLogin
from django.contrib import messages
from functools import wraps

class LoginView(View):
    def get(self, request):
        return render(request, 'Login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            ContribLogin(request, user)
            group = user.groups.values_list('name', flat=True).first()

            if group == 'coordinator':
                return redirect('dashboard')
            elif group == 'audiometrist':
                return redirect('audiometry')
            elif group == 'optometrist':
                return redirect('optometry')
            elif group == 'vitals':
                return redirect('vitals')
            elif group == 'vitals1':
                return redirect('vitals1')
            else:
                return redirect('form')
        else:
            messages.error(request, "Invalid credentials")
            return render(request, 'Login.html')

def user_type_required(user_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name=user_type).exists():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You don't have permission to access this page.")
                return redirect('login')

        return _wrapped_view

    return decorator
