from django.db import models


class CommonPart(models.Model):
    create_data = models.DateField(auto_now_add=True)
    update_data = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
