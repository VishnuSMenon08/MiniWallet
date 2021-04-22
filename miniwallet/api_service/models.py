from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


ACCOUNT_STATUS = [('E','Enabled'),('D','Disabled')]
# Create your models here.
class Account(models.Model):
    id = models.CharField(max_length=50,default=uuid.uuid1(),primary_key = True)
    owned_by = models.CharField(max_length=50)
    status = models.CharField(max_length=10,choices=ACCOUNT_STATUS,default='D')
    changed_at = models.DateTimeField(auto_now=False,auto_now_add=False,null=True)
    balance = models.DecimalField(max_digits = 15,decimal_places=2)

    def create(self):
        if not self.balance:
            self.balance = 0
        self.save()
        token = CustAuthToken(user = self)
        token.save()
        return token

    def __str__(self):
        return "Account : {}".format(self.id)

class Transaction(models.Model):
    id = models.CharField(max_length=50,default = uuid.uuid1(),primary_key=True)
    transaction_by = models.ForeignKey(Account,on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20)
    transaction_time = models.DateTimeField(auto_now=False,auto_now_add=False,null=True)
    amount = models.DecimalField(max_digits = 15, decimal_places=2)
    reference_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "Transaction {}".format(self.id)

class CustAuthToken(models.Model):
    token_id = models.CharField(max_length=50,default=uuid.uuid1(),primary_key=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)

    def __str__(self):
        return "Token {}".format(self.token_id)


