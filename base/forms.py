from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", 'email', 'password1', 'password2']

    def clean_password2(self):
        return super().clean_password2()