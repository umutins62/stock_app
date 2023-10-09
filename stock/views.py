from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from stock.models import Stock, Transaction, MoneyTransaction, GeneralSettings
from .forms import *
from django.contrib import messages


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        stocks = Stock.objects.all()
        fullname = request.user.get_full_name()

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
        yuzde = (profit / total_result_buy) * 100

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
            'fullname': fullname,

        }

        return render(request, "index.html", context=context)
    else:
        return redirect('user_login')


def alis_satis_hesapla(Transaction):
    kar = (Transaction.sell_price - Transaction.buy_price) * Transaction.shares
    zarar = max(0, (Transaction.buy_price - Transaction.sell_price) * Transaction.shares)

    return kar, zarar


# Örnek kullanım:
# hisse = Hisse.objects.get(pk=1)
# alis_satis_hesapla(hisse)


def stock_list(request):
    fullname = request.user.get_full_name()
    stocks = Stock.objects.all()

    context = {
        'stocks': stocks,
        'fullname': fullname,
    }

    return render(request, "stock_list.html", context=context)


def track_list(request):
    stocks = Stock.objects.all()
    fullname = request.user.get_full_name()
    transactions_all = Transaction.objects.all()
    money_transactions = MoneyTransaction.objects.all()
    general_settings = GeneralSettings.objects.all()

    transactions_buy = Transaction.objects.all()
    transactions_sell = Transaction.objects.filter(status="1")

    total_result_buy = sum(row.buy_price * row.shares for row in transactions_buy)
    total_result_sell = sum(row.sell_price * row.shares for row in transactions_sell)

    profit = total_result_sell - total_result_buy

    context = {
        'stocks': stocks,
        'transactions_all': transactions_all,
        'transactions_buy': transactions_buy,
        'transactions_sell': transactions_sell,
        'total_result_buy': total_result_buy,
        'total_result_sell': total_result_sell,
        'profit': profit,
        'fullname': fullname,

    }

    return render(request, "track_list.html", context=context)


def principal(request):
    fullname = request.user.get_full_name()
    money_transactions = MoneyTransaction.objects.all()

    context = {
        'fullname': fullname,
        'money_transactions': money_transactions,
    }

    return render(request, "principal.html", context=context)


def settings(request):
    return render(request, "settings.html")


def account(request):
    firstname = request.user.first_name
    lastname = request.user.last_name
    email = request.user.email
    username = request.user.username

    fullname = request.user.get_full_name()

    context = {
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'username': username,
        'fullname': fullname,
    }

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]


        user = User.objects.create_user(username=username, email=email, first_name=first_name,last_name=last_name)
        user.save()
        return redirect("account")

    return render(request, "account.html", context=context)


def add_stock(request):
    fullname = request.user.get_full_name()
    stocks = Stock.objects.all()
    if request.method == 'POST':
        form = AddStockForm(request.POST or None)
        if form.is_valid():
            symbol = request.POST.get('symbol')
            name = request.POST.get('name')
            Stock.objects.create(
                symbol=symbol,
                name=name)

            messages.success(request, 'Stock bilginiz başarıyla gönderildi.')
            return redirect('stock_list')


        else:
            messages.error(request, 'Stock bilginiz kaydedilemedi.')

    else:
        form = AddStockForm()

    context = {
        'fullname': fullname,
        'stocks': stocks,
        "form": form,
    }
    return render(request, "add_stock.html", context=context)


def delete_item(request, id):
    item = Stock.objects.get(id=id)
    item.delete()
    messages.success(request, 'Stock bilginiz başarıyla silindi.')
    return redirect('stock_list')


def update_item(request, id):
    fullname = request.user.get_full_name()
    stock = Stock.objects.get(id=id)

    if request.method == 'POST':
        form = AddStockForm(request.POST or None, instance=stock)
        if form.is_valid():
            stock.symbol = form.cleaned_data['symbol']
            stock.name = form.cleaned_data['name']
            stock.save()
            messages.success(request, 'Stock güncellendi')
            return redirect('stock_list')

    else:
        form = AddStockForm(instance=stock)

    context = {
        'fullname': fullname,

        "form": form,
        "stock": stock,
    }

    return render(request, "update_stock.html", context)

# def add_principal(request):
#     principal = MoneyTransaction.objects.all()
#     if request.method == 'POST':
#         form = AddPrincipalForm(request.POST or None)
#         if form.is_valid():
#             user = request.POST.get('user')
#             amount = request.POST.get('amount')
#             transaction_type = request.POST.get('transaction_type')
#             transaction_date = request.POST.get('transaction_date')
#             principal.objects.create(
#                 user=user,
#                 amount=amount,
#                 transaction_type=transaction_type,
#                 transaction_date=transaction_date,
#
#                 )
#
#             messages.success(request, 'Principal bilginiz başarıyla gönderildi.')
#             return redirect('principal')
#
#
#         else:
#             messages.error(request, 'Principal bilginiz kaydedilemedi.')
#
#     else:
#         form = AddPrincipalForm()
#
#     context = {
#         'principal': principal,
#         "form": form,
#     }
#     return render(request, "add_principal.html", context=context)
