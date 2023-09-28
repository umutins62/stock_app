from django.shortcuts import render
from stock.models import Stock, Transaction, MoneyTransaction, GeneralSettings
from openpyxl import load_workbook
import pandas as pd



# Create your views here.
def index(request):
    stocks = Stock.objects.all()
    transactions = Transaction.objects.all()
    money_transactions = MoneyTransaction.objects.all()
    general_settings = GeneralSettings.objects.all()

    excel_file = 'stock.xlsx'
    excel_data = pd.read_excel(excel_file)
    print(excel_data)
    deger=1.00


    context = {
        'stocks': stocks,
        'transactions': transactions,
        'money_transactions': money_transactions,
        'general_settings': general_settings,
        'deger':deger,
    }

    return render(request, "index.html", context=context)
