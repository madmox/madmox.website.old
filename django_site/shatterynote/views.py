from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from shatterynote import settings
from shatterynote.models import Secret
from shatterynote.forms import NewSecretForm, SubmitPassphraseForm


def index(request):
    if request.method == 'POST':
        # HTTP method is POST, the user tries to create a new secret
        
        # Maps submitted data to the form object
        form = NewSecretForm(request.POST)
        
        # Validates form data
        if form.is_valid():
            # Form data is valid: we create the new secret
            passphrase = form.cleaned_data['passphrase']
            message = form.cleaned_data['message']
            secret = Secret.objects.create_secret(passphrase, message)
            secret.save()
            
            # Redirects the user to the secret status page so that
            # he can get the one-time U.R.L.
            secret_id = Secret.objects.encrypt_id(secret.pk)
            return HttpResponseRedirect(
                reverse('shatterynote:status', args=(secret_id,))
            )
        else:
            # Form data is invalid: let the function return the bound form
            # which contains the error messages
            pass
    else:
        # HTTP metod is GET, the user is just displaying the page
        # so we return an unbound form
        form = NewSecretForm()
    
    # Returns either a bound or unbound form, depending on HTTP method
    return render(request, 'shatterynote/index.html', {'form': form})


def status(request, secret_id):
    # Retrieves the secret public infos
    try:
        secret_id = Secret.objects.decrypt_id(secret_id)
    except ValueError:
        raise Http404()
    secret = get_object_or_404(Secret, pk=secret_id)
    secret_url = secret.get_url()

    return render(
        request, 'shatterynote/status.html',
        {'secret': secret, 'secret_url': secret_url}
    )


def secret(request, encrypted_data):
    template = 'shatterynote/secret.html'
    
    # Checks the secret exists
    secret_id, secret_key = Secret.objects.unpack_infos(encrypted_data)
    secret = get_object_or_404(Secret, pk=secret_id)
    
    if request.method == 'POST':
        # The user submitted a passphrase for this secret
        
        # Asserts the secret is indeed secure
        # If it isn't, redirects the user with a GET method
        if not secret.is_secure():
            return HttpResponseRedirect(request.get_full_path())
        
        # Maps submitted data to the form object
        form = SubmitPassphraseForm(secret, request.POST)
        
        # Validates form data (checks passphrase...)
        if form.is_valid():
            # Passphrase is valid, the secret is now unciphered
            return HttpResponseRedirect(request.get_full_path())
        else:
            # Passphrase is invalid: the function returns the bound form
            # which contains the error messages
            pass
        
        # Renders the secret's page, with error messages
        return render(request, template, {'form': form, 'message': None})
    else:
        # The user is trying to view the secret
        if secret.is_secure():
            # The secret is secured: it will not be displayed,
            # don't consume it
            form = SubmitPassphraseForm(secret)
            message = None
        else:
            # The secret is not secured: consume it!
            form = None
            message = secret.decrypt_message(secret_key)
            secret.delete()
        
        # Renders the secret's page, be it with the message or with
        # the passphrase form
        return render(request, template, {'form': form, 'message': message})
