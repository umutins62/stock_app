# Generated by Django 4.2.5 on 2023-09-29 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_alter_transaction_sell_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(blank=True, default='', help_text='Please enter your status', max_length=50, verbose_name='status'),
        ),
    ]
