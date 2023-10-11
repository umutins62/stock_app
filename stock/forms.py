
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from stock.models import Stock,Transaction,MoneyTransaction


class AddStockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'name']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email']

class TransactionForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ['user','stock', 'buy_price', 'sell_price',
                  'shares','status'
                  ]

    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.id)

class MoneytransactionForm(ModelForm):
    class Meta:
        model = MoneyTransaction
        fields = ['user', 'amount', 'transaction_type']

    def __init__(self, user, *args, **kwargs):
        super(MoneytransactionForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.id)




class UpdatetrackingForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['user', 'stock','sell_price','status'
                  ]

    def __init__(self, user, *args, **kwargs):
        super(UpdatetrackingForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.id)




class UpdateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user','buy_price','shares']

    new_shares = forms.IntegerField(label='New Shares')
    new_buy_price = forms.DecimalField(label='New Buy Price', max_digits=10, decimal_places=2)


    def __init__(self, user, *args, **kwargs):
        super(UpdateTransactionForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.id)