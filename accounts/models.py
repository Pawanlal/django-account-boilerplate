import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# https://stackoverflow.com/questions/45621300/auto-generating-username-when-adding-a-user-with-django
def set_username(sender, instance, **kwargs):
    if not instance.username:
        username = (instance.first_name + "." + instance.last_name).lower()
        counter = 1
        while User.objects.filter(username=username):
            username = username + str(counter)
        instance.username = username


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not first_name:
            raise ValueError("User must have first name")
        if not last_name:
            raise ValueError("User must have last name")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(verbose_name='email', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


models.signals.pre_save.connect(set_username, sender=User)


class HealthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pregnancies = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    glucose = models.PositiveIntegerField()
    skin_thickness = models.PositiveIntegerField()
    bmi = models.DecimalField(max_digits=5, decimal_places=2)  # Using DecimalField for BMI
    insulin = models.PositiveIntegerField()
    output = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.output = random.randint(0, 1)
        super().save(*args, **kwargs)
