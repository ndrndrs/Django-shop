from django.shortcuts import render

from .forms import RegistrationForm
from .models import User


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.phone = phone
            user.save()
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'account/register.html', context)


def login(request):
    return render(request, 'account/login.html')


def logout(request):
    return
