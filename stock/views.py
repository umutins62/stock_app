import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils import translation

from djangoStockApp import settings
from stock.models import Stock, Transaction, MoneyTransaction, GeneralSettings
from .forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def index(request):
    if request.user.is_authenticated:

        fullname = request.user.get_full_name()
        profile_settings = UserAdd.objects.filter(user=request.user)
        user = request.user

        context = {

            'fullname': fullname,
            'user': user,
            'profile_settings': profile_settings,

        }

        return render(request, "index3.html", context=context)
    else:
        return render(request, "index4.html")


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
    transactions_all = Transaction.objects.filter(user=request.user)

    transactions_buy = Transaction.objects.filter(user=request.user)
    transactions_sell = Transaction.objects.filter(user=request.user).filter(status="1")

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
    money_transactions = MoneyTransaction.objects.filter(user=request.user)

    context = {
        'fullname': fullname,
        'money_transactions': money_transactions,
    }

    return render(request, "principal.html", context=context)


# def settings(request):
#     context = {
#         # buraya ayarlarınızı ekleyin
#     }
#     return render(request, 'partials/_settings.html', context)


def account(request):
    fullname = request.user.get_full_name()

    user_additional_instance, created = UserAdd.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        form1 = userAddForm(request.POST, request.FILES, instance=user_additional_instance)

        if form.is_valid():
            form.save()
            if form1.is_valid():
                user_add = form1.save(commit=False)
                user_add.user = request.user
                user_add.save()
                return redirect('dashboard')
            ...

        else:
            # Eğer her iki formdan biri doğrulanmazsa bu durumu kullanıcıya belirtmek için bir hata mesajı ekleyebilirsiniz.
            messages.error(request, 'Formda hatalar bulunmaktadır. Lütfen tekrar deneyiniz.')

    else:
        form1 = userAddForm(instance=request.user)
        form = UserForm(instance=request.user)

    context = {
        'form': form,
        'form1': form1,
        'fullname': fullname,
    }

    return render(request, 'account.html', context=context)


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


# views.py


from django.contrib.auth.forms import PasswordChangeForm


def change_password(request):
    fullname = request.user.get_full_name()
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifre başarıyla güncellendi!')
            return redirect('account')
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        'form': form,
        'fullname': fullname,
    }
    return render(request, 'change_pass.html', context)


def add_transaction(request):
    fullname = request.user.get_full_name()
    form = TransactionForm(request.user)
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('track_list')

    context = {'form': form,
               'fullname': fullname, }
    return render(request, 'add_tracking.html', context)


def add_money(request):
    fullname = request.user.get_full_name()
    form = MoneytransactionForm(request.user)
    if request.method == 'POST':
        form = MoneytransactionForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('principal')

    context = {'form': form,
               'fullname': fullname, }
    return render(request, 'add_principal.html', context=context)


def update_money(request):
    fullname = request.user.get_full_name()
    if request.method == 'POST':
        form = MoneytransactionForm(request.user, request.POST, instance=request.user.moneytransaction_set.first())
        if form.is_valid():
            form.save()
            messages.success(request, 'İşlem başarıyla güncellendi')
            return redirect('principal')
    else:
        form = MoneytransactionForm(request.user, instance=request.user.moneytransaction_set.first())

    context = {
        'form': form,
        'fullname': fullname,
    }
    return render(request, 'update_principal.html', context=context)


def update_track(request, id):
    stock = Transaction.objects.get(id=id)
    fullname = request.user.get_full_name()
    if request.method == 'POST':
        form = UpdatetrackingForm(request.user, request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'İşlem başarıyla güncellendi')
            return redirect('track_list')
    else:
        form = UpdatetrackingForm(request.user, instance=stock)

    context = {
        'form': form,
        'fullname': fullname,
    }
    return render(request, 'update_track.html', context=context)


@login_required
def update_price(request, id):
    fullname = request.user.get_full_name()
    transaction = get_object_or_404(Transaction, id=id, user=request.user)

    if request.method == 'POST':
        form = UpdateTransactionForm(request.user, request.POST, instance=transaction)
        if form.is_valid():
            new_shares = form.cleaned_data['new_shares']
            new_buy_price = form.cleaned_data['new_buy_price']

            # Hesaplama yap ve güncelle
            total_shares = transaction.shares + new_shares
            new_avg_price = ((transaction.buy_price * transaction.shares) + (new_buy_price * new_shares)) / total_shares

            # Veritabanını güncelle
            transaction.shares = total_shares
            transaction.buy_price = new_avg_price
            transaction.save()

            return redirect('track_list')  # İsteğe bağlı: Başarılı güncelleme sayfasına yönlendirme

    else:
        form = UpdateTransactionForm(request.user, instance=transaction)

    return render(request, 'buy_track.html', {
        'form': form,
        'fullname': fullname,
    })


@staff_member_required()
def special_admin(request):
    if request.user.is_superuser:
        return redirect('admin:index')
    else:
        raise PermissionDenied


def app_settings(request):
    return render(request, 'settings.html')


def my_messages(request):
    return render(request, 'messages.html')


def my_notifications(request):
    return render(request, 'Notifications.html')


def dashboard(request):
    stocks = Stock.objects.all()

    fullname = request.user.get_full_name()

    money_transactions_all = MoneyTransaction.objects.filter(user=request.user)[0:5]
    # money_transactions_all = MoneyTransaction.objects.filter(user=request.user).order_by('-transaction_date')[0:5]

    transactions = Transaction.objects.filter(user=request.user).filter(status="0")
    transactions_count = Transaction.objects.filter(user=request.user).filter(status="0").count()
    transactions1 = Transaction.objects.filter(user=request.user, status=1)

    money_transactions_w = MoneyTransaction.objects.filter(user=request.user).filter(
        transaction_type__iexact="Withraw")
    money_transactions_d = MoneyTransaction.objects.filter(user=request.user).filter(
        transaction_type__iexact="Deposit")

    deposit_total = sum([d.amount for d in money_transactions_d])
    withdraw_total = sum([w.amount for w in money_transactions_w])
    money_transactions = withdraw_total - deposit_total

    trade_buy = Transaction.objects.filter(user=request.user)
    total_stock = 0
    for item in trade_buy:
        total_stock += item.shares * item.buy_price

    general_settings = GeneralSettings.objects.all()

    # image
    image = GeneralSettings.objects.get(name='invoice').image

    # total money

    total_result_buy = sum(row.buy_price * row.shares for row in transactions1)
    total_result_sell = sum(row.sell_price * row.shares for row in transactions1)
    profit = total_result_sell - total_result_buy
    try:  # try except bloğu eklendi
        yuzde = (profit / total_result_buy) * 100
    except ZeroDivisionError:
        yuzde = 0

    en_buyuk_profit = Transaction.objects.filter(user=request.user).order_by('-profit').first()
    en_kucuk_profit = Transaction.objects.filter(user=request.user).order_by('profit').first()

    user = request.user

    data = [float(t.profit) for t in transactions1]
    # labels = [t.stock.symbol for t in transactions1]
    labels = [t.transaction_edit_date.strftime('%d-%m-%Y') for t in transactions1]

    net_total = money_transactions + profit

    context = {
        'stocks': stocks,
        'transactions': transactions,
        'money_transactions': money_transactions,
        'general_settings': general_settings,
        'image': image,
        'total_sum': money_transactions,
        'profit': profit,
        'yuzde': yuzde,
        'en_buyuk_profit': en_buyuk_profit,
        'en_kucuk_profit': en_kucuk_profit,
        'fullname': fullname,
        'user': user,
        'transactions_count': transactions_count,
        'money_transactions_all': money_transactions_all,
        'transactions1': transactions1,
        'total_stock': total_stock,
        'deposit_total': deposit_total,
        'withdraw_total': withdraw_total,
        'labels_json': labels,
        'data_json': data,
        'net_total': net_total,
    }

    return render(request, 'dashboard/dashboard.html', context=context)
