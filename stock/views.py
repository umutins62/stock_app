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

    context = {
        'stocks': stocks,
        'transactions': transactions,
        'money_transactions': money_transactions,
        'general_settings': general_settings,
        'image': image,
        'total_sum': total_sum,
        'profit': profit,
        'yuzde': yuzde
    }

    return render(request, "index.html", context=context)

# def islem_kaydet(hisse_adi, alim_satim, miktar, fiyat):
#     yeni_islem = Transaction.objects.create(hisse_adi=hisse_adi, alim_satim=alim_satim, miktar=miktar, fiyat=fiyat)
#
#     if alim_satim == 'ALIM':
#         Anapara.objects.filter(pk=1).update(tutar=F('tutar') + miktar * fiyat)
#
#     if alim_satim == 'SATIM':
#         Anapara.objects.filter(pk=1).update(tutar=F('tutar') - miktar * fiyat)
