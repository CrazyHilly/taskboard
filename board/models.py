from django.db import models
from django.urls import reverse
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Task(models.Model):
    TASK_STATUS_CHOICES = [
        ("new", "New"),
        ("active", "In progress"),
        ("completed", "Completed")
    ]

    TASK_PRIORITY_CHOICES = [
        ("critical", "Very important"),
        ("high", "Important"),
        ("medium", "Normal"),
        ("low", "Optional"),
    ]

    name = models.CharField(max_length=60)
    priority = models.CharField(
        max_length=20, choices=TASK_PRIORITY_CHOICES, default="medium"
        )
    status = models.CharField(
        max_length=20, choices=TASK_STATUS_CHOICES, default="new"
        )

    tags = models.ManyToManyField(Tag, related_name="tasks")
    description = models.TextField(max_length=5000, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    due_by = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        old_status = Task.objects.get(pk=self.pk)
        if old_status != "completed" and self.status == "completed":
            self.completed_at = timezone.now()

        if self.status in ("new", "active") and self.completed_at:
            self.completed_at = None

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("board:task-detail", args=[self.pk])
    
    class Meta:
        ordering = [models.F("due_by").asc(nulls_last=True)]
