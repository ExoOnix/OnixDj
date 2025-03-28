from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Todo(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="todos"
    )

    def __str__(self):
        return self.title
