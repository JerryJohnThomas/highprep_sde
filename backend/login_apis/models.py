from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser



# Create your models here.
# we will be making our customer user for easy authentication and login for this purpose. 
# class PersonInfo(models.Model):
#     password = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


# this is the manager for this user 
class CustomPersonManager(BaseUserManager):

    # this function will save the user given the following details 
    def create_user(self, name, email, phone_number, age, person_type,bike_details, password=None, password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            phone_number = phone_number,
            age = age,
            person_type = person_type,
            bike_details = bike_details,
        )

        # here we will save the password and the save the user in database 
        user.set_password(password)
        user.save(using=self._db)
        return user


    # in case of a superuser the following function will be there 
    def create_superuser(self,  name, email, phone_number, age, person_type,bike_details,  password=None, password2=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email = email,
            password=password,
            name = name,
            phone_number = phone_number,
            age = age,
            person_type = person_type,
            bike_details=bike_details,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class PersonInfo(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    name = models.TextField(max_length=200)
    phone_number = models.CharField(max_length=12)
    age = models.IntegerField()
    person_type = models.CharField(max_length=100)
    bike_details = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomPersonManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'age', 'person_type', 'bike_details']   

    def __str__(self):
        return self.email


    # this is talking about the allowed permission for this current user 
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin;

    # this is module level permission this will be open to all as the app information can be fetched by everyone
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
