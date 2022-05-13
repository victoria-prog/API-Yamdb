from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MyUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = ('email',)