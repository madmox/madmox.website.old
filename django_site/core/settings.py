"""
Settings for the core app (used by any other app)
"""

import os
from core.tools import get_env_var


# Piwik is the trafic monitoring tool of the site, it should be enabled in
# production only
ENABLE_PIWIK = (get_env_var('DJANGO_ENABLE_PIWIK', required=False, default='False') == 'True')
