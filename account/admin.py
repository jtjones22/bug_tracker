from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account, Ticket

# Register your models here.

admin.site.register(Account, UserAdmin)
admin.site.register(Ticket)
