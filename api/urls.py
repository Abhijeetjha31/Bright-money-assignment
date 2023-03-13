from django.urls import path
from . import views

urlpatterns = [
    path('api/register-user/', views.register_user, name='user-registration'),
    path('api/apply-loan/', views.apply_loan, name='apply-loan'),
    path('api/make-payment/', views.make_payment, name='make-payment'),
    path('api/view-loan/<uuid:loan_id>/', views.loan_detail, name='view-loan'),
]
