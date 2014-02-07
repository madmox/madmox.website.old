from django import forms
from shatterynote import settings
from shatterynote.helpers import hash_passphrase


class NewSecretForm(forms.Form):
    """
    This form is used when a user wants to create a new secret
    """
    
    message = forms.CharField(max_length=25000, widget=forms.Textarea)
    passphrase = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder':
                'Un mot de passe ou une phrase difficile à deviner'
            }
        )
    )


class SubmitPassphraseForm(forms.Form):
    """
    This form is used when a user wants to uncipher its secret when
    the secret's creator set a passphrase for it
    """
    
    passphrase = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':
                "Le mot de passe ou la phrase secrète que vous a communiqué l'émetteur du lien"
            }
        )
    )
    
    def __init__(self, secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret = secret
    
    def clean_passphrase(self):
        if self.secret.is_secure():
            # Checks the submitted passphrase is the same as the one stored
            # in database
            passphrase = self.cleaned_data['passphrase']
            if self.secret.is_passphrase_valid(passphrase):
                # Passphrases are identics: uncipher the message and removes
                # the passphrase from the secret
                self.secret.decrypt_message_with_passphrase()
                self.secret.save()
            else:
                # Passphrases are differents: wrong input
                raise forms.ValidationError("La phrase secrète est invalide.")
