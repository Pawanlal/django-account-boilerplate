from django import forms
from django.contrib.auth import get_user_model, authenticate

from .models import HealthRecord

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['pregnancies', 'age', 'glucose', 'skin_thickness', 'bmi', 'insulin', 'bp', 'func']
