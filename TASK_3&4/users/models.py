from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class extendeduser(models.Model):

    GENDER_CHOICES = (
        
            ('M', 'Male'),
            ('F', 'Female'),
        )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=10,null=True,default=" ")
    last_name = models.CharField(max_length=12,null=True,default=" ")
    place = models.CharField(max_length=12,null=True,default=" ")
    phone_num = models.CharField(max_length=15)
    gender = models.CharField(max_length=12, choices=GENDER_CHOICES,null=True,default=" ")
    age = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    user = models.OneToOneField(User,on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.username}'