# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='nom', max_length=50)),
                ('order', models.IntegerField(verbose_name="ordre d'affichage", validators=[django.core.validators.MinValueValidator(0)], unique=True)),
                ('image', models.ImageField(verbose_name='image', blank=True, upload_to='recipes/categories/')),
                ('created_at', models.DateTimeField(verbose_name='date de création', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='date de mise à jour', auto_now=True)),
            ],
            options={
                'verbose_name': 'catégorie',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='nom', max_length=100)),
                ('order', models.IntegerField(verbose_name="ordre d'affichage", validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'ingrédient',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='nom', max_length=50)),
                ('nb_persons', models.IntegerField(verbose_name='nombre de personnes', validators=[django.core.validators.MinValueValidator(1)])),
                ('preparation_time', models.IntegerField(verbose_name='temps de préparation (en minutes)', validators=[django.core.validators.MinValueValidator(1)])),
                ('total_time', models.IntegerField(verbose_name='temps total (en minutes)', validators=[django.core.validators.MinValueValidator(1)])),
                ('image', models.ImageField(verbose_name='image', blank=True, upload_to='recipes/recipes/')),
                ('created_at', models.DateTimeField(verbose_name='date de création', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='date de mise à jour', auto_now=True)),
                ('category', models.ForeignKey(to='recipes.Category', verbose_name='catégorie')),
            ],
            options={
                'verbose_name': 'recette',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='libellé', max_length=200)),
                ('order', models.IntegerField(verbose_name="ordre d'affichage", validators=[django.core.validators.MinValueValidator(0)])),
                ('recipe', models.ForeignKey(to='recipes.Recipe', verbose_name='recette')),
            ],
            options={
                'verbose_name': 'étape',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='nom', max_length=100)),
                ('order', models.IntegerField(verbose_name="ordre d'affichage", validators=[django.core.validators.MinValueValidator(0)])),
                ('recipe', models.ForeignKey(to='recipes.Recipe', verbose_name='recette')),
            ],
            options={
                'verbose_name': 'ustensile',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tool',
            unique_together=set([('recipe', 'order')]),
        ),
        migrations.AlterUniqueTogether(
            name='step',
            unique_together=set([('recipe', 'order')]),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(to='recipes.Recipe', verbose_name='recette'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='ingredient',
            unique_together=set([('recipe', 'order')]),
        ),
    ]
