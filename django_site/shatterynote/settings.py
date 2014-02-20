"""
Django settings for shatterynote app.
"""

from django.core.exceptions import ImproperlyConfigured


def __import_key():
    from core.tools import get_env_var
    utf8_b64_key = get_env_var('DJANGO_AES_KEY')
    try:
        b64_key = utf8_b64_key.encode('utf8')
        import base64
        return base64.standard_b64decode(b64_key)
    except:
        raise ImproperlyConfigured("'DJANGO_AES_KEY' setting is invalid")

AES_KEY = __import_key()
