from django.forms import ModelForm, CheckboxSelectMultiple, DateTimeInput, Textarea

from board.models import Task, Tag, Comment


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ("name", "priority", "tags", "description", "due_by")
        widgets = {
            "tags": CheckboxSelectMultiple, 
            "due_by": DateTimeInput(attrs={"type": "datetime-local"})
            }


class TagCreateForm(ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        all_colors = dict(Tag.TAG_COLOR_CHOICES).keys()
        used_colors = Tag.objects.values_list("color", flat=True)
        available_colors = [(c, c) for c in all_colors if c not in used_colors]

        if self.instance and self.instance.color:
            available_colors.append((self.instance.color, self.instance.color))

        self.fields["color"].choices = available_colors


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment", )
        labels = {"comment": ""}
        widgets = {
            "comment": Textarea(attrs={
                "rows": 2,
                "placeholder": "Add comment here...",
                "class": "comment-input",
            }),
        }
