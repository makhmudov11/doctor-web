import logging

logger = logging.getLogger(__name__)


def generate_code(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


import random


def generate_public_id(model, field="public_id", start=1000000, end=9999999):
    while True:
        public_id = random.randint(start, end)
        if not model.objects.filter(**{field: public_id}).exists():
            return public_id


def generate_unique_order_id():
    from apps.order.models import Order
    while True:
        length = random.choice([5, 6])
        order_id = ''.join(str(random.randint(0, 9)) for _ in range(length))
        if not Order.objects.filter(order_id=order_id).exists():
            return order_id


def generate_unique_balance_id():
    from apps.transactions.models import UserUniqueBalanceID

    while True:
        balance_id = ''.join(random.choices('0123456789', k=7))
        if not UserUniqueBalanceID.objects.filter(balance_id=balance_id).exists():
            return balance_id