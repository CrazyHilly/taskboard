from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Task(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_by = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completion_time = models.DateTimeField(blank=True, null=True)
    in_progress = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag, related_name="tasks")
