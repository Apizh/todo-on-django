from django.forms import ModelForm

from todo_home.models import TodoUser


class TodoUserForm(ModelForm):
    class Meta:
        model = TodoUser
        fields = ['title', 'status', 'priority']