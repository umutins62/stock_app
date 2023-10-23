# Generated by Django 4.2.5 on 2023-10-20 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0008_alter_moneytransaction_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(blank=True, choices=[('buy', '0'), ('sell', '1')], default='', help_text='Please enter your status', max_length=50, verbose_name='status'),
        ),
    ]