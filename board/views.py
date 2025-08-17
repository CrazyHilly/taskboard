from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from board.forms import TaskCreateForm
from board.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"grouped_tasks": {
            "new_tasks": Task.objects.filter(status="new"),
            "active_tasks": Task.objects.filter(status="active"),
            "completed_tasks": Task.objects.filter(status="completed"),
        }, "today": timezone.now()})
        return context


class TaskDetailView(generic.DetailView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("board:task-list")


class TagListView(generic.ListView):
    model = Tag
