import random
import pickle as pkl
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages

from .forms import UserRegisterForm, UserLoginForm, HealthRecordForm

User = get_user_model()

recommendation = {
    "Food Recommendation": [
        "Control Carbohydrate Intake",
        "Choose Lean Proteins",
        "Healthy Fats",
        "Fiber-Rich Foods",
        "Balanced Meals",
        "Regular Meal Times",
        "Monitor Your Blood Sugar",
        "Stay Hydrated",
        "Limit Alcohol Intake",
        "Individualized Plan"
        ],
    "Life style recommendation": [
        "Regular Physical Activity",
        "Weight Management",
        "Balanced Diet",
        "Regular Blood Sugar Monitoring",
        "Medication Management",
        "Stress Management",
        "Smoking Cessation",
        "Alcohol in Moderation",
        "Regular Healthcare Check-ups",
        "Education and Support",
        "Foot Care",
        "Hydration"
        ]
}


def home(request):
    if request.user.is_anonymous:
        return redirect('/login')
    
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)

        if form.is_valid():
                Pregnancies = form.cleaned_data['pregnancies']
                Age = form.cleaned_data['age']
                Glucose = form.cleaned_data['glucose']
                SkinThickness = form.cleaned_data['skin_thickness']
                BMI = form.cleaned_data['bmi']
                Insulin = form.cleaned_data['insulin']
                bp = form.cleaned_data['bp']
                func = form.cleaned_data['func']

                model = pkl.load(open('accounts/model/svm_model.pkl', 'rb'))
                scaler = pkl.load(open('accounts/model/scaler.pkl', 'rb'))

                input_features = [[Pregnancies, Glucose, bp, SkinThickness, Insulin, BMI, func, Age]]
                input_features = scaler.transform(input_features)
                prediction = model.predict(input_features)

                if BMI > 30 and prediction == 0:
                    prediction = 1

                health_record = form.save(commit=False)
                health_record.user = request.user
                health_record.output = prediction
                health_record.save()

                if prediction == 1:
                    # Randomly select two items from Food Recommendation
                    food_recommendation = random.sample(recommendation["Food Recommendation"], 2)

                    # Randomly select two items from Lifestyle Recommendation
                    lifestyle_recommendation = random.sample(recommendation["Life style recommendation"], 2)

                    message = "Diabetic\nFood Recommendation: {}\nLife style recommendation: {}".format(
    ", ".join(food_recommendation),
    ", ".join(lifestyle_recommendation)
)
                    messages.success(request, message)
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


