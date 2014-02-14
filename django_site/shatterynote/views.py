from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_control

from shatterynote import settings
from shatterynote.models import Secret
from shatterynote.forms import NewSecretForm, SubmitPassphraseForm


def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def unpad_base64_string(data):
    if isinstance(data, str):
        return data.replace('=', '')
    else:
        return data.replace(b'=', b'')


def pad_base64_string(data):
    # Restores equal signs to the string
    if len(data) % 3 == 0:
        pass
    elif len(data) % 3 == 1:
        if isinstance(data, str):
            data = data + '=='
        else:
            data = data + b'=='
    elif len(data) % 3 == 2:
        if isinstance(data, str):
            data = data + '='
        else:
            data = data + b'='
    return data
    


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
            secret_id = unpad_base64_string(secret_id)
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


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def status(request, base64_data):
    base64_data = pad_base64_string(base64_data)
    secret, secret_id, secret_url = None, None, None
    
    # Parses and validates URL infos
    try:
        secret_id = Secret.objects.decrypt_id(base64_data)
    except ValueError:
        # Invalid HMAC
        pass
    
    # Gets secret if it exists
    if secret_id is not None:
        secret = get_object_or_none(Secret, pk=secret_id)
        if secret is not None:
            url_segment = secret.get_url_segment()
            if url_segment is not None:
                # Strips equal signs from the string
                url_segment = unpad_base64_string(url_segment)
                relative_url = reverse(
                    'shatterynote:secret',
                    args=(url_segment,)
                )
                secret_url = request.build_absolute_uri(relative_url)

    return render(
        request, 'shatterynote/status.html',
        {'secret': secret, 'secret_url': secret_url}
    )


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def secret(request, base64_data):
    template = 'shatterynote/secret.html'
    base64_data = pad_base64_string(base64_data)
    found, form, message = False, None, None
    
    # Checks the secret exists
    try:
        secret_id, secret_key = Secret.objects.unpack_infos(base64_data)
        secret = Secret.objects.get(pk=secret_id)
        found = True
    except (ValueError, Secret.DoesNotExist):
        # Invalid HMAC or unknown secret ID
        pass
    
    if found:
        if request.method == 'POST':
            # The user submitted a passphrase for this secret
            
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
        else:
            # The user is trying to view the secret
            if secret.is_secure():
                # The secret is secured: it will not be displayed,
                # don't consume it
                form = SubmitPassphraseForm(secret)
            else:
                # The secret is not secured: consume it!
                message = secret.decrypt_message(secret_key)
                secret.delete()
        
    # Renders the secret's page, with error messages
    return render(
        request, template,
        {'form': form, 'message': message, 'found': found}
    )
