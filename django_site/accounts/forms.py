from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms


class UserChangeForm(forms.ModelForm):
    """
    Defines an update form for any user profile (hides authorization
    informations
    """
    error_messages = {
        'duplicate_username': ("Ce nom d'utilisateur est déjà utilisé.")
    }
    
    username = forms.RegexField(
        label="Nom d'utilisateur", max_length=30, regex=r"^[\w.@+-]+$",
        error_messages={
            'invalid': ("Ce champ ne peut contenir que des caractères "
                         "alphanumériques et les caractères @/./+/-/_.")
        }
    )
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        if self.instance.username == username:
            return username
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )
