from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks'
    )

    class Status(models.TextChoices):
        TODO = ('todo', 'To Do')
        IN_PROGRESS = ('in_progress', 'In Progress')
        DONE = ('done', 'Done')

    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.TODO
    )

    def __str__(self):
        return self.title
