# Generated by Django 4.2.5 on 2023-10-05 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0006_transaction_profit'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', help_text='Please enter your name', max_length=50, verbose_name='Name')),
                ('value', models.CharField(blank=True, default='', help_text='Please enter your value', max_length=50, verbose_name='Value')),
                ('image', models.ImageField(blank=True, help_text='Please enter your image', null=True, upload_to='images/', verbose_name='Image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Setting',
                'verbose_name_plural': 'User Settings',
                'ordering': ['-name'],
            },
        ),
    ]
