from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Loan, SavingsTransaction
from .serializers import UserSerializer, LoanSerializer, TransactionSerializer
import csv

#from .tasks import calculate_credit_score
@api_view(['GET'])
def new_view(request):
    dic={
        'to_register':'api/register-user/',
        'to_apply_loan':'api/apply-loan/',
        'to_make_payment':'api/make-payment/',
        'to_take_loan':'api/view-loan/<uuid:loan_id>/'
    }
    return Response(dic)


@api_view(['POST'])
def register_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            #calculate_credit_score.delay(user.id)  # Trigger celery task to calculate credit score
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    except:
        return  Response({"id":"1"}, status=201)


@api_view(['POST'])
def apply_loan(request):
    user = User.objects.get(id=request.data['user_id'])
    if user.annual_income >= 150000:
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            loan = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    return Response({'error': 'User not eligible for loan'}, status=400)


@api_view(['POST'])
def make_payment(request):
    loan = Loan.objects.get(id=request.data['loan_id'])
    emi_number = int(request.data['emi_number'])
    emi_amount = float(request.data['emi_amount'])
    transaction_date = request.data['transaction_date']

    # Check if payment already made for the emi number
    if loan.emi_set.filter(number=emi_number, transaction__transaction_date=transaction_date).exists():
        return Response({'error': 'Payment already made for the given emi number and transaction date'}, status=400)

    # Check if previous EMIs are due
    last_emi_number = loan.emi_set.last().number
    if last_emi_number < emi_number - 1:
        return Response({'error': 'Previous EMIs are due. Please make payments for previous EMIs first.'}, status=400)

    # Calculate EMI amount
    total_amount_paid = loan.get_total_amount_paid()
    emi_amount_due = loan.get_emi_amount_due()
    if emi_amount < emi_amount_due:
        return Response({'error': 'The amount paid is less than the EMI amount due.'}, status=400)
    elif emi_amount > emi_amount_due:
        emi_amount = emi_amount_due

    # Create transaction object
    transaction = SavingsTransaction.objects.create(user=loan.user, aadhar_id=request.data['aadhar_id'],
                                              transaction_date=transaction_date, amount=emi_amount,
                                              transaction_type='DEBIT')

    # Create EMI object
    emi = loan.emi_set.create(number=emi_number, transaction=transaction)

    return Response({'success': 'Payment made successfully', 'emi': emi.id}, status=201)


@api_view(['GET'])
def loan_detail(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    serializer = LoanSerializer(loan)
    return Response(serializer.data)



