from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('groups', 'company')
