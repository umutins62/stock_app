from django.shortcuts import render
from stock.models import Stock, Transaction, MoneyTransaction, GeneralSettings

# Create your views here.
def index(request):
    stocks = Stock.objects.all()
    transactions = Transaction.objects.all()
    money_transactions = MoneyTransaction.objects.all()
    general_settings = GeneralSettings.objects.all()

    context = {
        'stocks': stocks,
        'transactions': transactions,
        'money_transactions': money_transactions,
        'general_settings': general_settings,
    }

    return render(request, "index.html", context=context)
