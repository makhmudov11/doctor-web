from rest_framework import serializers

from apps.transactions.models import Transactions


class UserTransactionHistorySerializer(serializers.ModelSerializer):
    data_type = serializers.CharField(default='balance', read_only=True)
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = Transactions
        fields = ['data_type', 'created_at', 'balance_id', 'amount', 'provider', 'status']
