from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    
    def get_name(self):
        username = self.username
        if len(username) < 12:
            return username
        else:
            return username[:11] + '.'
