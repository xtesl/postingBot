from django.db import models
from account.models import CustomUser
from django.utils.timezone import now

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


