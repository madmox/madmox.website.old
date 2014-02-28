from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'},
        name='login'
    ),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        name='logout'
    ),
    url(
        r'^password/change/$',
        'django.contrib.auth.views.password_change',
        {
            'template_name': 'accounts/password_change.html',
            'post_change_redirect': 'accounts:password-change-done'
        },
        name='password-change'
    ),
    url(
        r'^password/change/done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'accounts/password_change_done.html'},
        name='password-change-done'
    ),
    url(
        r'^password/reset/$',
        'django.contrib.auth.views.password_reset',
        {
            'template_name': 'accounts/password_reset.html',
            'email_template_name': 'accounts/password_reset_email.html',
            'subject_template_name': 'accounts/password_reset_subject.txt',
            'post_reset_redirect': 'accounts:password-reset-done',
            'from_email': 'madmox.fr <noreply@madmox.fr>'
        },
        name='password-reset'
    ),
    url(
        r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'accounts/password_reset_done.html'},
        name='password-reset-done'
    ),
    url(
        r'^password/reset/confirm/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {
            'template_name': 'accounts/password_reset_confirm.html',
            'post_reset_redirect': 'accounts:password-reset-complete'
        },
        name='password-reset-confirm'
    ),
    url(
        r'^password/reset/complete/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'accounts/password_reset_complete.html'},
        name='password-reset-complete'
    ),
)
