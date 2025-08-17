from django.urls import reverse_lazy
from django.views import generic

from board.forms import TaskCreateForm
from board.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task


class TaskDetailView(generic.DetailView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("board:task-list")


class TagListView(generic.ListView):
    model = Tag
