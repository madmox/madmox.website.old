from core import settings


def piwik(request):
    return { 'piwik_enabled': settings.ENABLE_PIWIK }
