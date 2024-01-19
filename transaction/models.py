from django.db import models
from account.models import UserAccount
from book.models import Book
from django.contrib.auth.models import User
from .constants import TRANSACTION_TYPE
# Create your models here.

class Transaction(models.Model):
    user=models.ForeignKey(UserAccount,related_name='transactions',on_delete = models.CASCADE, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    book=models.ForeignKey(Book,on_delete = models.CASCADE,null=True)
    is_returned=models.BooleanField(default=False)

    def __str__(self):
        return str(self.transaction_type)

