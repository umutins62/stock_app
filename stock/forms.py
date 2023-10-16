from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from stock.models import Stock, Transaction, MoneyTransaction


class AddStockForm(ModelForm):
    symbol = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Stock
        fields = ['symbol', 'name']


class UserForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class TransactionForm(ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    STATUS = (
        ('1', 'Satıldı'),
        ('0', 'Satılmadı'),
    )
    status = forms.ChoiceField(
        choices=STATUS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    buy_price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    sell_price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    shares = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Transaction
        fields = ['user', 'stock', 'buy_price', 'sell_price',
                  'shares', 'status'
                  ]

    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.id)


class MoneytransactionForm(ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    STATUS = (
        ('Withraw', 'Withraw'),
        ('Deposit', 'Deposit'),
    )
    transaction_type = forms.ChoiceField(
        choices=STATUS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amount = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = MoneyTransaction
        fields = ['user', 'amount', 'transaction_type']

    def __init__(self, user, *args, **kwargs):
        super(MoneytransactionForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.id)


class UpdatetrackingForm(ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sell_price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    STATUS = (
        ('1','Satıldı'),
        ('0','Satılmadı'),
    )
    status = forms.ChoiceField(
        choices=STATUS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Transaction
        fields = ['user', 'stock', 'sell_price', 'status'
                  ]

    def __init__(self, user, *args, **kwargs):
        super(UpdatetrackingForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.id)


class UpdateTransactionForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    buy_price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    shares = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Transaction
        fields = ['user', 'buy_price', 'shares']

    new_shares = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    new_buy_price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super(UpdateTransactionForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.id)


from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
