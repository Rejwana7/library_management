from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE,GENDER_TYPE


# Create your models here.
class UserAccount(models.Model):
    user= models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    account_type=models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    balance=models.DecimalField(default=0,max_digits=15,decimal_places=2)
    initial_deposite_date= models.DateField(auto_now_add=True)
    
     #kkhon account khulbe
    def __str__(self):
        return {self.user.username} -{self.id}
