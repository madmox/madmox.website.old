# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Secret'
        db.create_table('shatterynote_secret', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('encrypted_message', self.gf('django.db.models.fields.BinaryField')(blank=True, null=True)),
            ('passphrase_hash', self.gf('django.db.models.fields.BinaryField')(blank=True, null=True)),
            ('aes_key', self.gf('django.db.models.fields.BinaryField')(blank=True, null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
        ))
        db.send_create_signal('shatterynote', ['Secret'])


    def backwards(self, orm):
        # Deleting model 'Secret'
        db.delete_table('shatterynote_secret')


    models = {
        'shatterynote.secret': {
            'Meta': {'object_name': 'Secret'},
            'aes_key': ('django.db.models.fields.BinaryField', [], {'blank': 'True', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'encrypted_message': ('django.db.models.fields.BinaryField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passphrase_hash': ('django.db.models.fields.BinaryField', [], {'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['shatterynote']