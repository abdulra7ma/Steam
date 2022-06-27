from collections import UserList
from django.contrib import admin

from chat.models import Message, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Message)