import random
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

CITIES =  (('bishkek', 'Bishkek'),
            ('osh', 'Osh'),
            ('jalal-abad', 'Jalal-Abad'),
            ('karakol', 'Karakol'),
            ('naryn', 'Naryn'),
            ('batken', 'Batken'),
            ('talas', 'Talas'),)


RELATIONSHIP_STATUSES = (
            ('searching', 'Searching'),
            ('in-a-relationship', 'In a relationship'),
            ('married', 'Married'),
            ('not-interested', 'Not interested'),
        )

GENDERS = (
    ('male', 'Мужчина'),
    ('female', 'Женщина'),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username должен быть указан')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(username, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to='users/', null=True, blank=True)
    email = models.EmailField('Электронная почта:')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    first_name = models.CharField(
        max_length=120,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name="Фамилия"
    )
    surname = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name="Отчество"
    )
    city = models.CharField(max_length=20, choices=CITIES, null=True, blank=True)
    relationship_status = models.CharField(max_length=20, choices=RELATIONSHIP_STATUSES, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDERS, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class EmailConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=6, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = f"{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)
