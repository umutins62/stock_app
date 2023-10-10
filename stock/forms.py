
from django.forms import ModelForm
from django.contrib.auth.models import User

from stock.models import Stock


class AddStockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'name']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email']





