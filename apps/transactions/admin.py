from django.contrib import admin
from .models import Transactions, UserUniqueBalanceID
from paycomuz.models import Transaction

admin.site.unregister(Transaction)
@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'balance_id',
        'request_id',
        'request_id',
        'amount',
        'provider',
        'status',
        'perform_datetime',
        'cancel_datetime',
        'created_datetime',
        'reason',
        'state',
    ]

    list_filter = [
        'provider',
        'status',
        'state',
        'perform_datetime',
        'cancel_datetime',
        'created_datetime',
    ]

    search_fields = [
        '_id',
        'request_id',
        'balance_id__balance_id',
    ]

    readonly_fields = [
        'perform_datetime',
        'cancel_datetime',
        'created_datetime',
        'state',
    ]

@admin.register(UserUniqueBalanceID)
class UserUniqueBalanceIDAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance_id', 'balance')
    search_fields = ('user__username', 'balance_id')