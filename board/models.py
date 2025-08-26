from tkinter import CASCADE
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Tag(models.Model):
    TAG_COLOR_CHOICES = [
        ("blue", "blue"),
        ("brown", "brown"),
        ("gray", "gray"),
        ("green", "green"),
        ("olive", "olive"),
        ("orange", "orange"),
        ("pink", "pink"),
        ("purple", "purple"),
        ("teal", "teal"),
        ("turquoise", "turquoise"),
        ("red", "red"),
        ("yellow", "yellow"),
    ]
    name = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=20, unique=True, choices=TAG_COLOR_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Task(models.Model):
    TASK_STATUS_CHOICES = [
        ("new", "New"),
        ("active", "In progress"),
        ("completed", "Completed")
    ]

    TASK_PRIORITY_CHOICES = [
        (0, "critical"),
        (1, "high"),
        (2, "medium"),
        (3, "low"),
    ]

    name = models.CharField(max_length=150)
    priority = models.IntegerField(
        choices=TASK_PRIORITY_CHOICES, 
        default="2",
        validators=[MinValueValidator(0), MaxValueValidator(3)]
        )
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default="new")

    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True, null=True)
    description = models.TextField(max_length=5000, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    due_by = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        object = Task.objects.filter(pk=self.pk).first()
        if object and object.status != "completed" and self.status == "completed":
            self.completed_at = timezone.now()

        if self.status in ("new", "active") and self.completed_at:
            self.completed_at = None
        
        self.name = self.name.capitalize()
        
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("board:task-detail", args=[self.pk])
    
    class Meta:
        ordering = ["priority", models.F("due_by").asc(nulls_last=True), "created_at"]

    def __str__(self):
        return f"{self.pk}: {self.name}"


class Comment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="comments", 
        default=None, blank=True, null=True
        )
    comment = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
