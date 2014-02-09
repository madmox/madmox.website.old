# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Category', fields ['slug']
        db.create_unique('recipes_category', ['slug'])

        # Adding unique constraint on 'Recipe', fields ['slug']
        db.create_unique('recipes_recipe', ['slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Recipe', fields ['slug']
        db.delete_unique('recipes_recipe', ['slug'])

        # Removing unique constraint on 'Category', fields ['slug']
        db.delete_unique('recipes_category', ['slug'])


    models = {
        'recipes.category': {
            'Meta': {'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'unique': 'True', 'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        },
        'recipes.ingredient': {
            'Meta': {'object_name': 'Ingredient', 'unique_together': "(('recipe', 'order'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Recipe']"})
        },
        'recipes.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nb_persons': ('django.db.models.fields.IntegerField', [], {}),
            'preparation_time': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'unique': 'True', 'max_length': '50'}),
            'total_time': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        },
        'recipes.step': {
            'Meta': {'object_name': 'Step', 'unique_together': "(('recipe', 'order'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Recipe']"})
        },
        'recipes.tool': {
            'Meta': {'object_name': 'Tool', 'unique_together': "(('recipe', 'order'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Recipe']"})
        }
    }

    complete_apps = ['recipes']