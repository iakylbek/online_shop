import jwt
import datetime

from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise TypeError("Please, enter your email.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    DoesNotExist = None
    USER_GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(max_length=64, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)

    birthday = models.DateField(null=True, default=None, blank=True)

    gender = models.CharField(max_length=16, choices=USER_GENDER)
    phone = models.CharField(max_length=64, unique=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    avatar = models.ImageField(upload_to='users/uploads/%Y/%m/%d/',
                               null=True, blank=True, max_length=100)
    is_banned = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'birthday',
                       'gender', 'phone', 'country', 'city', 'address']

    objects = MyUserManager()

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def token(self):
        return self._generate_jwt_token()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
