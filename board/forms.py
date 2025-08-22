from django.forms import ModelForm, CheckboxSelectMultiple, DateTimeInput

from board.models import Task


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ("name", "priority", "tags", "description", "due_by")
        widgets = {
            "tags": CheckboxSelectMultiple, 
            "due_by": DateTimeInput(attrs={"type": "datetime-local"})
            }
        