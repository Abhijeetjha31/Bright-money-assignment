from django.db import models
from django.contrib.auth.models import User

class SavingsTransaction(models.Model):
    aadhar_id = models.CharField(max_length=12)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhar_id = models.CharField(max_length=12)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    credit_score = models.IntegerField(null=True, blank=True)
    email=models.EmailField(max_length=40)

class Loan(models.Model):
    id=models.UUIDField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=4, decimal_places=2)
    term_period = models.IntegerField()
    disbursement_date = models.DateField()
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)

# Create your models here.
