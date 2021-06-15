from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.fields import EmailField
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, full_name, mobile, address, password=None):
        if not email:
            raise ValidationError("Email is required")
        if not full_name:
            raise ValidationError("Name is required")
        if not mobile:
            raise ValidationError("Mobile is required")
        if not address:
            raise ValidationError("Address is required")

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            mobile=mobile,
            address=address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, mobile, address, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            mobile=mobile,
            address=address,
            password=password,
            full_name=full_name
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address", max_length=60, unique=True)
    full_name = models.CharField(verbose_name="name", max_length=40)
    mobile = models.CharField(max_length=10, verbose_name="mobile")
    address = models.CharField(max_length=100, verbose_name="address")
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_name', 'mobile', 'address']

    objects = MyUserManager()

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Ewaste(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    item_name = models.CharField(max_length=30)
    item_description = models.CharField(max_length=100)
    item_image = models.ImageField(upload_to='media')
    date = models.DateField()

    # overwriting delete method to delete pics from media
    def delete(self, *args, **kwargs):
        self.item_image.delete()
        super().delete(*args, **kwargs)


class PickedEwaste(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    item_name = models.CharField(max_length=30)
    item_description = models.CharField(max_length=100)
    item_image = models.ImageField(upload_to='media')
    date = models.DateField()
    picked_date = models.DateField()


class Bills(models.Model):
    bill_id = models.IntegerField()
    bill_amount = models.IntegerField()
    bill_month = models.CharField(max_length=10)
    bill_date = models.DateField()
