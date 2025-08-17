from django.forms import ModelForm, CheckboxSelectMultiple

from board.models import Task


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {"tags": CheckboxSelectMultiple}
