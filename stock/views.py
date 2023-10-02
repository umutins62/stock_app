from django.db.models import Sum
from django.forms import models
from django.shortcuts import render
from stock.models import Stock, Transaction, MoneyTransaction, GeneralSettings
from openpyxl import load_workbook
import pandas as pd


# Create your views here.
def index(request):
    stocks = Stock.objects.all()

    transactions = Transaction.objects.filter(status="0")
    transactions1 = Transaction.objects.filter(status="1")

    money_transactions = MoneyTransaction.objects.all()
    general_settings = GeneralSettings.objects.all()

    # image
    image = GeneralSettings.objects.get(name='invoice').image

    # total money

    total_sum = MoneyTransaction.objects.aggregate(total_sum=Sum('amount'))['total_sum']
    total_result_buy = sum(row.buy_price * row.shares for row in transactions1)
    total_result_sell = sum(row.sell_price * row.shares for row in transactions1)
    profit = total_result_sell - total_result_buy
    yuzde = (profit / total_result_buy)*100

    en_buyuk_profit = Transaction.objects.all().order_by('-profit').first()
    en_kucuk_profit = Transaction.objects.all().order_by('profit').first()




    context = {
        'stocks': stocks,
        'transactions': transactions,
        'money_transactions': money_transactions,
        'general_settings': general_settings,
        'image': image,
        'total_sum': total_sum,
        'profit': profit,
        'yuzde': yuzde,
        'en_buyuk_profit': en_buyuk_profit,
        'en_kucuk_profit': en_kucuk_profit,

    }

    return render(request, "index.html", context=context)


def alis_satis_hesapla(Transaction):
    kar = (Transaction.sell_price - Transaction.buy_price) * Transaction.shares
    zarar = max(0, (Transaction.buy_price - Transaction.sell_price) * Transaction.shares)

    return kar, zarar

# Örnek kullanım:
# hisse = Hisse.objects.get(pk=1)
# alis_satis_hesapla(hisse)


