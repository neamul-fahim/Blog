from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    # def create_user(self, email, password=None, **extra_fields):
    #     if not email:
    #         raise ValueError("Email field can't be empty!")

    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)

    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if not email:
            raise ValueError("Email field can't be empty!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, verbose_name='password')
    username = models.CharField(max_length=100, blank=True, null=True)
    first_login = models.DateTimeField(auto_now_add=True,
                                       blank=True, null=True, verbose_name='first login')
    last_login = models.DateTimeField(auto_now=True,
                                      blank=True, null=True, verbose_name='last login')
    is_staff = models.BooleanField(default=False, verbose_name='staff status')
    is_superuser = models.BooleanField(
        default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')
    groups = models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                    related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')
    user_permissions = models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                              related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # related to creating superuser

    def __str__(self):
        return f"User(email={self.email}, is_staff={self.is_staff}, is_superuser={self.is_superuser})"

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True


class OtpVerificationManager(BaseUserManager):
    def create_unverified_user(self, email, password, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.expires_at = timezone.now()+timezone.timedelta(minutes=1)
        user.set_password(password)
        user.save(using=self._db)

        return user


class OtpVerification(AbstractBaseUser):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, verbose_name='password')
    username = models.CharField(max_length=100, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    expires_at = models.DateTimeField(verbose_name='expires at')

    USERNAME_FIELD = 'email'
    objects = OtpVerificationManager()

    def __str__(self):
        return f"User(email={self.email}, username={self.username})"
