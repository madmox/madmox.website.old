# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations
import django.core.validators


def create_permission(apps, schema_editor):
    """Create the share 'can browse' global permission"""
    
    ContentType = apps.get_model("contenttypes.ContentType")
    Permission = apps.get_model("auth.Permission")
    
    ct, created = ContentType.objects.get_or_create(
        name="global_permission",
        app_label='share',
        model=''
    )
    
    perm, created = Permission.objects.get_or_create(
        codename='can_browse',
        content_type=ct,
        defaults={'name': 'Can browse'}
    )


def delete_permission(apps, schema_editor):
    """Delete the share 'can browse' global permission"""
    
    ContentType = apps.get_model("contenttypes.ContentType")
    Permission = apps.get_model("auth.Permission")
    
    # Gets content type
    ct = ContentType.objects.get(
        name="global_permission",
        app_label='share',
        model=''
    )
    
    # Deletes permission
    Permission.objects.get(
        codename='can_browse',
        content_type=ct
    ).delete()
    
    # Deletes content type
    ct.delete()


class Migration(migrations.Migration):

    # Forces contenttypes and auth apps to migrate before this on,
    # as well as any custom auth user model
    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_permission, delete_permission),
    ]
