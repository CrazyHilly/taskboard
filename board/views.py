from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from board.forms import TaskCreateForm, TagCreateForm
from board.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "grouped_tasks": {
            "new_tasks": {
                "tasks": Task.objects.filter(status="new"), 
                "status": "Open"
                },
            "active_tasks": {
                "tasks": Task.objects.filter(status="active"), 
                "status": "In Progress"
                },
            "completed_tasks": {
                "tasks": Task.objects.filter(status="completed"), 
                "status": "Done"
                }},
            "today": timezone.now()
            })
        return context


class TaskDetailView(generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"today": timezone.now()})
        return context


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("board:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskCreateForm

    def get_success_url(self):
        return reverse_lazy("board:task-detail", kwargs={"pk": self.object.pk})


class TagListView(generic.ListView):
    model = Tag


class TagCreateView(generic.CreateView):
    model = Tag
    form_class = TagCreateForm
    success_url = reverse_lazy("board:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("board:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("board:tag-list")
