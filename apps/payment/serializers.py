from rest_framework import serializers

from apps.transactions.models import TransactionProvider


class PaymentProviderSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
    provider_name = serializers.ChoiceField(TransactionProvider.choices, required=True)