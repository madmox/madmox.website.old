from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms


class UserChangeForm(forms.ModelForm):
    """
    Defines an update form for any user profile (hides authorization
    informations
    """
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
