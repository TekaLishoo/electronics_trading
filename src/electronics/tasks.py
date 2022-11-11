from celery import shared_task
from src.electronics.models import NetworkObject
from random import choice
from djmoney.money import Money
from decimal import Decimal


@shared_task
def increase_debt():
    """
    Task runs every 3 hours.
    It will increase a debt of network objects by a random number.
    """

    objects = NetworkObject.objects.all()

    for obj in objects:
        obj.debt = Money(
            obj.debt.amount + Decimal(choice(range(5, 500))), "BYN"
        )
        obj.save()


@shared_task
def decrease_debt():
    """
        Task runs every day at 6.30.
        It will decrease a debt of network objects by a random number.
        """

    objects = NetworkObject.objects.all()

    for obj in objects:
        amount_to_decrease = choice(range(100, 10000))
        if Decimal(amount_to_decrease) <= obj.debt.amount:
            obj.debt = Money(
                obj.debt.amount - Decimal(amount_to_decrease), "BYN"
            )
        else:
            obj.debt = Money(Decimal(0), "BYN")
        obj.save()
