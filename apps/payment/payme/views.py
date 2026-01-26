from django.utils.datetime_safe import datetime
from paycomuz import Paycom
from paycomuz.status import TRANSACTION_NOT_FOUND, TRANSACTION_NOT_FOUND_MESSAGE, UNABLE_TO_PERFORM_OPERATION_MESSAGE, \
    UNABLE_TO_PERFORM_OPERATION, CANCEL_TRANSACTION_CODE, CLOSE_TRANSACTION
from paycomuz.views import MerchantAPIView

from apps.transactions.models import UserUniqueBalanceID, Transactions, TransactionChoices
from apps.utils.validates import parse_payme_time


class CheckBalanceID(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        try:
            UserUniqueBalanceID.objects.get(
                balance_id=account['balance_id']
            )
        except UserUniqueBalanceID.DoesNotExist:
            return self.ORDER_NOT_FOND

        if not isinstance(amount, int) or amount <= 0:
            return self.INVALID_AMOUNT
        return self.ORDER_FOUND

    def successfully_payment(self, account, transaction, *args, **kwargs):
        user_balance = transaction.balance_id
        user_balance.balance += transaction.amount
        user_balance.save(update_fields=['balance'])

    def cancel_payment(self, account, transaction, *args, **kwargs):
        pass


class PayComAPIView(MerchantAPIView):
    VALIDATE_CLASS = CheckBalanceID

    def check_perform_transaction(self, validated_data):
        super().check_perform_transaction(validated_data)

    def create_transaction(self, validated_data):
        params = validated_data['params']
        balance = UserUniqueBalanceID.objects.get(balance_id=params['account']['balance_id'])
        payme_tx_id = params['id']

        transaction_obj, created = Transactions.objects.get_or_create(
            payme_transaction_id=payme_tx_id,
            defaults={
                'balance_id': balance,
                'amount': params['amount'],
                'state': 1,
                'created_datetime': parse_payme_time(params['time']),
                'request_id': validated_data.get('id')
            }
        )

        self.reply = {
            "result": {
                "create_time": int(transaction_obj.created_datetime.timestamp() * 1000),
                "transaction": str(transaction_obj.id),
                "state": transaction_obj.state
            },
            "error": None,
            "id": transaction_obj.request_id
        }
        return self.reply

    def perform_transaction(self, validated_data):
        payme_transaction_id = validated_data['params']['id']
        request_id = validated_data['id']
        try:
            obj = Transactions.objects.get(payme_transaction_id=payme_transaction_id)
            if obj.state not in [CANCEL_TRANSACTION_CODE]:
                obj.state = CLOSE_TRANSACTION
                obj.status = TransactionChoices.SUCCESS
                if not obj.perform_datetime:
                    obj.perform_datetime = datetime.now()
                    self.VALIDATE_CLASS().successfully_payment(account=validated_data['params'], transaction=obj)

                self.reply = dict(result=dict(
                    transaction=str(obj.id),
                    perform_time=int(obj.perform_datetime.timestamp() * 1000),
                    state=obj.state
                ))
            else:
                obj.status = TransactionChoices.FAILED

                self.reply = dict(error=dict(
                    id=request_id,
                    code=UNABLE_TO_PERFORM_OPERATION,
                    message=UNABLE_TO_PERFORM_OPERATION_MESSAGE
                ))
            obj.save()
        except Transactions.DoesNotExist:
            self.reply = dict(error=dict(
                id=request_id,
                code=TRANSACTION_NOT_FOUND,
                message=TRANSACTION_NOT_FOUND_MESSAGE
            ))