"""
WSGI config for madmox_website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from core.tools import set_env_vars

projdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
set_env_vars(projdir)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
