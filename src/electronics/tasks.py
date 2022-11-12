from celery import shared_task
from src.electronics.models import NetworkObject
from random import choice
from djmoney.money import Money
from decimal import Decimal
from django.core.mail import EmailMultiAlternatives
from electronics_trading.settings import EMAIL_HOST_USER
from qrcode import make
from functools import lru_cache
from email.mime.image import MIMEImage
from io import BytesIO


@shared_task
def increase_debt():
    """
    Task runs every 3 hours.
    It will increase a debt of network objects by a random number.
    """

    objects = NetworkObject.objects.all()

    for obj in objects:
        obj.debt = Money(obj.debt.amount + Decimal(choice(range(5, 500))), "BYN")
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
            obj.debt = Money(obj.debt.amount - Decimal(amount_to_decrease), "BYN")
        else:
            obj.debt = Money(Decimal(0), "BYN")
        obj.save()


@shared_task
def send_mail_func(email, contacts):
    """
    Task for send a mail with a QR code in attachment.
    """

    mail_subject = "QR code from electronics app"
    mail_body = "There is a QR code in attachment"
    message = EmailMultiAlternatives(
        subject=mail_subject,
        body=mail_body,
        from_email=EMAIL_HOST_USER,
        to=[
            email,
        ],
    )
    message.mixed_subtype = "related"
    message.attach(qr_data(contacts))

    message.send(fail_silently=False)


@lru_cache()
def qr_data(contacts):
    """
    Returns an attachment with a QR code
    formed from given contacts.
    """

    qr_code = make(str(contacts))
    buff = BytesIO()
    qr_code.save(buff, format="PNG")
    qr_attachment = MIMEImage(buff.getvalue(), _subtype="png")
    qr_attachment.add_header("Content-ID", "<qr_code>")
    return qr_attachment
