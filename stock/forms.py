from django import forms
from django.core.mail import send_mail, EmailMessage

from djangoStockApp import settings
from django.forms import ModelForm

from stock.models import *


class AddStockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'name']


# class AddPrincipalForm(ModelForm):
#     class Meta:
#         model = MoneyTransaction
#         fields = ['user', 'amount', 'transaction_type']
