from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

citizen_id_validator = RegexValidator(
    r'^\d{13}$',
    'Citizen ID must be exactly 13 digits long and only contain numbers.'
)

mobile_validator = RegexValidator(
    r'^\d{10}$',
    'Mobile number must be exactly 10 digits long and only contain numbers.'
)

class Customer(AbstractUser):
    citizen_id = models.CharField(
        max_length=13, 
        unique=True, 
        validators=[citizen_id_validator]
    )
    mobile = models.CharField(
        max_length=10,
        validators=[mobile_validator]
    )
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
