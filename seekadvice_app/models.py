from django.db import models
from django.contrib.auth.models import User, AbstractUser
from cloudinary.models import CloudinaryField
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

#https://tech.serhatteker.com/post/2020-01/email-as-username-django/

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    displayname = models.CharField(max_length=50)
    jobtitle = models.CharField(max_length=50)
    short_description = models.CharField(max_length=250)
    linkedin_name = models.CharField(max_length=50, blank = True)
    github_name = models.CharField(max_length=50, blank = True)
    user_avatar = CloudinaryField('image')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ServiceAreas(models.Model):
    serviceareas = models.CharField(max_length=50, blank = True)

    class Meta:
        ordering = ['serviceareas']

    def __str__(self):
        return self.serviceareas


class ServiceTechnology(models.Model):
    servicetechnology = models.CharField(max_length=50, blank = True)

    class Meta:
        ordering = ['servicetechnology']

    def __str__(self):
        return self.servicetechnology


class ServiceAreasTechExpert(models.Model):
    serviceareas = models.CharField(max_length=50, blank = True)

    class Meta:
        ordering = ['serviceareas']

    def __str__(self):
        return self.serviceareas


class ServiceOffer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    consulting = models.BooleanField(default=False)
    generaladvice = models.BooleanField(default=False)
    talk = models.BooleanField(default=False)
    price = models.IntegerField(blank=True, default=0)
    description = models.CharField(max_length=250, blank = True)
    user_service_areas = models.ManyToManyField(ServiceAreas, blank = True, through='ServiceAreasRole')
    user_service_technology = models.ManyToManyField(ServiceTechnology, blank = True)

    class Meta:
        ordering = ['-id']
        #ordering = ['?']

    def __str__(self):
        return self.user.email


class ServiceOfferTechExpert(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    consulting = models.BooleanField(default=False)
    generaladvice = models.BooleanField(default=False)
    talk = models.BooleanField(default=False)
    price = models.IntegerField(blank=True, default=0)
    description = models.CharField(max_length=250, blank = True)
    user_service_areas = models.ManyToManyField(ServiceAreasTechExpert, blank = True)
    user_service_technology = models.ManyToManyField(ServiceTechnology, blank = True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.user.email

#https://docs.djangoproject.com/en/dev/topics/db/models/#extra-fields-on-many-to-many-relationships
class ServiceAreasRole(models.Model):
    role_serviceoffer = models.ForeignKey(ServiceOffer, on_delete=models.CASCADE)
    role_serviceareas = models.ForeignKey(ServiceAreas, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank = True)

    class Meta:
        ordering = ['-role']

