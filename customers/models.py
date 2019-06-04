from django.db import models
from django.contrib.auth import get_user_model


class Customer(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    photo = models.ImageField(blank=True, null=True, upload_to='customer/%Y/%m')
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   related_name="customers_created")
    modified_by = models.ForeignKey(get_user_model(),
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name="customers_modified")

