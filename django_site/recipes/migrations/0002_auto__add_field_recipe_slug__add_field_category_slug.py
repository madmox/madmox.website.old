# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models, transaction
from recipes.models import Category, Recipe


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Category.slug'
        db.add_column('recipes_category', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Fills default slug field for categories
        with transaction.atomic():
            categories_noslug = Category.objects.select_for_update().filter(slug__exact='')
            for category in categories_noslug:
                category.save()

        # Adding field 'Recipe.slug'
        db.add_column('recipes_recipe', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Fills default slug field for recipes
        with transaction.atomic():
            recipes_noslug = Recipe.objects.select_for_update().filter(slug__exact='')
            for recipe in recipes_noslug:
                recipe.save()
        

    def backwards(self, orm):
        # Deleting field 'Category.slug'
        db.delete_column('recipes_category', 'slug')

        # Deleting field 'Recipe.slug'
        db.delete_column('recipes_recipe', 'slug')


    models = {
        'recipes.category': {
            'Meta': {'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'recipes.ingredient': {
            'Meta': {'unique_together': "(('recipe', 'order'),)", 'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Recipe']"})
        },
        'recipes.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nb_persons': ('django.db.models.fields.IntegerField', [], {}),
            'preparation_time': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'total_time': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'recipes.step': {
            'Meta': {'unique_together': "(('recipe', 'order'),)", 'object_name': 'Step'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Recipe']"})
        },
        'recipes.tool': {
            'Meta': {'unique_together': "(('recipe', 'order'),)", 'object_name': 'Tool'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Recipe']"})
        }
    }

    complete_apps = ['recipes']