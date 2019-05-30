from django.db import models


class Customer(models.Model):
    photo = models.ImageField(upload_to='customer/%Y/%m', default='img/None/no-img.jpg')

