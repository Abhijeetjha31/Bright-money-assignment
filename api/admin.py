from django.contrib import admin
from .models import Loan,Payment,SavingsTransaction,UserProfile

admin.site.register(Loan)
admin.site.register(Payment)
admin.site.register(SavingsTransaction)
admin.site.register(UserProfile)