from django.urls import path

from .views import home, register, login_user, logout_user

app_name = 'accounts'
urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name="logout"),
]
