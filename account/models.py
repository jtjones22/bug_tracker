from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

import datetime

# Create your models here.


class Account(AbstractUser):
    pass


class Ticket(models.Model):
    CHOICES = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
        ('Invalid', 'Invalid'),
    )
    title = models.CharField(max_length=30)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    time = models.DateTimeField(
        default=datetime.datetime.now,
        blank=True
        )
    description = models.TextField()

    status = models.CharField(
        choices=CHOICES,
        max_length=20,
        default='New'
        )
    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned',
        null=True,
        blank=True,
        )
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='completed',
        null=True,
        blank=True,
        )

    def __str__(self):
        return f'{self.title} | {self.submitted_by} | {self.status}'
