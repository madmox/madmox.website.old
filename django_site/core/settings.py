"""
Settings for the core app (used by any other app)
"""

import os


# Piwik is the trafic monitoring tool of the site, it should be enabled in
# production only
ENABLE_PIWIK = (os.environ.get('DJANGO_ENABLE_PIWIK') != None)
