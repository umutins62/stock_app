from django.contrib import admin
from stock.models import *

# Register your models here.
@admin.register(Stock)
class stockAdmin(admin.ModelAdmin):
    list_display = ['id','symbol','name'
                    ]
    list_editable = ['symbol','name']

    class Meta:
        model = Stock
@admin.register(Transaction)
class transactionAdmin(admin.ModelAdmin):
    list_display = ['id','user','stock','buy_price','sell_price','shares','profit','status','transaction_edit_date',
                    'transaction_date'

                    ]
    list_editable = ['sell_price','shares','profit','status']
    list_filter = ['user','stock','status']

    class Meta:
        model = Transaction

@admin.register(MoneyTransaction)
class moneytransactionAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','transaction_type','transaction_date'

                    ]
    list_editable = ['amount','transaction_type']

    class Meta:
        model = MoneyTransaction

@admin.register(GeneralSettings)
class generalsettingsAdmin(admin.ModelAdmin):
    list_display = ['id','name','value','image'

                    ]
    list_editable = ['name','value','image']

    class Meta:
        model = GeneralSettings

@admin.register(UserSettings)
class usersettingsAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'name', 'value', 'image'

                    ]
    list_editable = ['user','name', 'value', 'image']

    class Meta:
        model = GeneralSettings




