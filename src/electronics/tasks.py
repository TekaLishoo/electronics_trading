from celery import shared_task
from src.electronics.models import NetworkObject
from random import randint


@shared_task
def increase_debt():
    """
    Task runs every 3 hours.
    It will increase a debt of network objects by a random number.
    """

    objects = NetworkObject.objects.all()

    for obj in objects:
        obj.debt += randint(5, 500)
        obj.save()

