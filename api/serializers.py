from rest_framework import serializers
from .models import User, Loan, SavingsTransaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'
        # fields = ('name', 'email', 'annual_income', 'credit_score')

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('loan_type', 'loan_amount', 'interest_rate', 'term_period', 'disbursement_date', 'emi_amount')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsTransaction
        fields = ( 'aadhar_id', 'transaction_date', 'amount', 'transaction_type')

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email')

class ApplyLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('loan_type', 'loan_amount')

class MakePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsTransaction
        fields = ('aadhar_id', 'transaction_date', 'amount', 'transaction_type')

class LoanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('loan_type', 'loan_amount', 'interest_rate', 'term_period', 'disbursement_date', 'emi_details')
