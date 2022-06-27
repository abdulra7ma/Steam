from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import datetime
from django.contrib.auth import get_user_model
from steam import settings
from django.core.cache import cache

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.user.email

    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.email)

    def online(self):
            if self.last_seen():
                now = datetime.datetime.now()
                if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                    return False
                else:
                    return True
            else: 
                return False


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    ir_read = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.message


    class Meta:
        ordering = ('timestamp',)
