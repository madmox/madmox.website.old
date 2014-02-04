"""
Django settings for shatterynote app.
"""


def __import_key():
    import os
    utf8_b64_key = os.environ['DJANGO_AES_KEY']
    b64_key = utf8_b64_key.encode('utf8')
    import base64
    return base64.standard_b64decode(b64_key)

AES_KEY = __import_key()
