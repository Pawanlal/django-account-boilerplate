import pickle as pkl
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages

from .forms import UserRegisterForm, UserLoginForm, HealthRecordForm

User = get_user_model()


def home(request):
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)

        if form.is_valid():
            with open('/home/pawan/Drive/lancemeup/django-account-boilerplate/accounts/model/diabetes_disease_prediction.pkl', 'rb') as f:
                Model = pkl.load(f)
                
                Pregnancies = form.cleaned_data['pregnancies']
                Age = form.cleaned_data['age']
                Glucose = form.cleaned_data['glucose']
                SkinThickness = form.cleaned_data['skin_thickness']
                BMI = form.cleaned_data['bmi']
                # Insulin = form.cleaned_data['insulin']

                Model.predict([[Pregnancies, Glucose, SkinThickness, BMI, Age]])

                health_record = form.save(commit=False)
                health_record.user = request.user
                health_record.save()

                if health_record.output == 1:
                    messages.success(request, 'Diabetic')
                else:
                    messages.success(request, 'Not Diabetic')
    else:
        form = HealthRecordForm()
    
     #list all the health records
    health_records = request.user.healthrecord_set.all()
    context = {'health_records': health_records, "form": form}

    return render(request, 'accounts/home.html', context)


def register(request):
    context = {}
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
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
                print('Invalid credentials')
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
