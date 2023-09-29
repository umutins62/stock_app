from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Stock(models.Model):
    symbol = models.CharField(
        verbose_name='Symbol',
        default='',
        max_length=50,
        blank=True,
        help_text='Please enter your symbol')

    name = models.CharField(
        verbose_name='Name',
        default='',
        max_length=50,
        blank=True,
        help_text='Please enter your name')

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        ordering = ['-name']


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)

    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE)

    buy_price = models.DecimalField(
        verbose_name='Buy Price',
        max_digits=10,
        decimal_places=2)
    sell_price = models.DecimalField(
        verbose_name='Sell Price',
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    status=models.CharField(
        verbose_name='status',
        default='',
        max_length=50,
        blank=True,
        help_text='Please enter your status')



    shares = models.IntegerField(
        verbose_name='Shares',

    )

    transaction_date = models.DateTimeField(
        verbose_name='Transaction Date',
        auto_now_add=True,
        blank=True,
        help_text='Please enter your transaction date')


    transaction_edit_date= models.DateTimeField(
        verbose_name='Transaction Edit Date',
        auto_now=True,
        blank=True,
        help_text='Please enter your transaction edit date'
    )


    def __str__(self):
        return self.stock.name

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-transaction_date']

class MoneyTransaction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    amount = models.DecimalField(
        verbose_name='Amount',
        max_digits=10,
        decimal_places=2)
    transaction_type = models.CharField(
        verbose_name='Transaction Type',
        default='',
        max_length=10)
    transaction_date = models.DateTimeField(
        verbose_name='Transaction Date',
        auto_now_add=True,
        blank=True,
        help_text='Please enter your transaction date'

    )

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Money Transaction'
        verbose_name_plural = 'Money Transactions'
        ordering = ['-transaction_date']

class GeneralSettings(models.Model):
    name = models.CharField(
        verbose_name='Name',
        default='',
        max_length=50,
        blank=True,
        help_text='Please enter your name')
    value = models.CharField(
        verbose_name='Value',
        default='',
        max_length=50,
        blank=True,
        help_text='Please enter your value')
    image = models.ImageField(
        verbose_name='Image',
        upload_to='images/',
        blank=True,
        null=True,
        help_text='Please enter your image')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'General Setting'
        verbose_name_plural = 'General Settings'
        ordering = ['-name']
