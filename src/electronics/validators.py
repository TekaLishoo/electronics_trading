from datetime import date
from rest_framework import serializers


def validate_presentation_date(value):
    if value.year < 1500 or value.year > (date.today().year + 2):
        raise serializers.ValidationError(
            "Please enter a valid date of product presentation."
        )
