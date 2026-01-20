from django.contrib.auth import get_user_model
from django.db import models

from apps.utils.base_models import CreateUpdateBaseModel
from apps.utils.generate_code import generate_unique_balance_id

User = get_user_model()


class TransactionChoices(models.TextChoices):
    PROCESSING = 'processing', 'Processing'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'
    CANCELLED = 'cancelled', 'Cancelled'


class TransactionProvider(models.TextChoices):
    PAYME = 'payme', 'Payme'


class Transactions(CreateUpdateBaseModel):
    balance_id = models.ForeignKey('UserUniqueBalanceID', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='users_transactions')
    payme_transaction_id = models.CharField(max_length=255, null=True)
    request_id = models.IntegerField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.IntegerField(blank=True, null=True)  # tranzaksiya qaysi bosqichadaligi raqami
    provider = models.CharField(choices=TransactionProvider.choices, default=TransactionProvider.PAYME, max_length=20)
    status = models.CharField(choices=TransactionChoices.choices, default=TransactionChoices.PROCESSING, max_length=55)
    perform_datetime = models.DateTimeField(null=True, blank=True)
    cancel_datetime = models.DateTimeField(null=True, blank=True)
    created_datetime = models.DateTimeField(null=True, blank=True)
    reason = models.IntegerField(null=True, blank=True)  # nimaga bekor qilingani haqida raqam

    def __str__(self):
        return f"{self.id}"

    class Meta:
        db_table = 'transaction'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']


class UserUniqueBalanceID(CreateUpdateBaseModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='user_balance_id')
    balance_id = models.CharField(max_length=10, unique=True, db_index=True)
    balance = models.PositiveBigIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.balance_id:
            self.balance_id = generate_unique_balance_id()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'balance_id'
        verbose_name = 'Balance ID'
        ordering = ['id']

    def __str__(self):
        return f"{self.balance_id} ---------- {self.user}"
