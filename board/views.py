from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic

from board.forms import TaskCreateForm, TagCreateForm, CommentForm
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
        context.update({
            "today": timezone.now(),
            "comment_form": CommentForm(),
            })
        return context
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.save()
            return redirect(reverse_lazy("board:task-detail", kwargs={"pk": task.pk}))
        
        context = self.get_context_data()
        context["comment_form"] = form
        return self.render_to_response(context)


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("board:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskCreateForm

    def get_success_url(self):
        return reverse_lazy("board:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("board:task-list")


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


def change_task_status(request, pk):
    task = Task.objects.get(pk=pk)

    if task.status == "new":
        task.status = "active"
    elif task.status == "active":
        task.status = "completed"
    else: 
        task.status = "new"

    task.save()
    
    return redirect(request.META.get(
        "HTTP_REFERER", reverse("board:task-detail", kwargs={"pk": pk})
        ))
