# Generated by Django 4.2.5 on 2023-10-20 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0010_alter_transaction_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAdd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Please enter your image', null=True, upload_to='images/', verbose_name='Image')),
                ('phone', models.CharField(blank=True, default='', help_text='Please enter your phone', max_length=50, verbose_name='Phone')),
                ('address', models.CharField(blank=True, default='', help_text='Please enter your address', max_length=50, verbose_name='Address')),
                ('user_save_date', models.DateTimeField(auto_now_add=True, help_text='Please enter your user save date', verbose_name='User Save Date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Add',
                'verbose_name_plural': 'User Adds',
                'ordering': ['-user_save_date'],
            },
        ),
    ]
