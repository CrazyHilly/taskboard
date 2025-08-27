from django.urls import path

from board.views import TagCreateView, TagDeleteView, TagListView, TagUpdateView, \
                        TaskDetailView, TaskListView, TaskCreateView, TaskUpdateView, \
                        change_task_status


urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path(
        "tasks/<int:pk>/change-status/", 
        change_task_status, 
        name="change-task-status"
        ),
    path("tasks/new/", TaskCreateView.as_view(), name="task-create"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/new/", TagCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update/", TagUpdateView.as_view(), name="tag-update"),
    path("tags/<int:pk>/delete/", TagDeleteView.as_view(), name="tag-delete"),
]

app_name = "board"
