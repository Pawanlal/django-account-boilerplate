import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout

from .forms import UserRegisterForm, UserLoginForm

User = get_user_model()


def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    context = {}
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        client_key = request.POST['g-recaptcha-response']
        secret_key = '6Lf0Yf4ZAAAAAO2lS3tsx-ZXnowy3qLbW0N-xq5l'
        captchadata = {
            'secret': secret_key,
            'response': client_key
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchadata)
        response = json.loads(r.text)
        verify = response['success']
        print('Your success is: ', verify)
        if verify and form.is_valid():
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            return redirect('/login')
        else:
            context['registration_form'] = form
    else:
        form = UserRegisterForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = authenticate(email=request.POST['email'], password=request.POST['password'])

            if user:
                print(user)
                login(request, user)
                return redirect('/')
            else:
                print('Invalid Credentials')
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('/login')
