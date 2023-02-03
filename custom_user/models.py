from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, password=None):
        if not first_name:
            raise ValueError(" User must have first name")

        if not email:
            raise ValueError(" User must have an email ")

        if not username:
            raise ValueError("User must have an username ")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        superuser = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
        )

        superuser.is_superadmin = True
        superuser.is_admin = True
        superuser.is_active = True
        superuser.is_staff = True
        superuser.set_password(password)
        superuser.save(using=self.db)

        return superuser


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=30)

    user_join = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now_add=True)
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username', 'first_name', 'last_name'
    ]

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
