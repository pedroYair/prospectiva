# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreLargo', models.CharField(max_length=50)),
                ('nombreCorto', models.CharField(max_length=10)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('informacion', models.TextField(null=True, blank=True)),
                ('codigo_Estudio', models.PositiveIntegerField(default=1)),
                ('creador', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Actor',
                'verbose_name_plural': 'Actores',
            },
        ),
        migrations.CreateModel(
            name='Cuestion_Estrategica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cuestion', models.TextField(max_length=200)),
                ('codigo_Estudio', models.PositiveIntegerField(default=1)),
                ('actor', models.ForeignKey(blank=True, to='mactor.Actor', null=True)),
                ('creador', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Cuestion_estrategica',
                'verbose_name_plural': 'Cuestiones_estrategicas',
            },
        ),
        migrations.CreateModel(
            name='Estudio_Mactor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.PositiveIntegerField(default=1)),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=2000, null=True, blank=True)),
                ('fecha_inicio', models.DateField(auto_now=True, null=True)),
                ('fecha_final', models.DateField(auto_now=True, null=True)),
                ('estado', models.BooleanField()),
                ('codigo_proy', models.PositiveIntegerField(default=1)),
                ('coordinadores', models.ManyToManyField(related_name='mactor_coordinadores_set', verbose_name=b'Coordinadores', to=settings.AUTH_USER_MODEL)),
                ('expertos', models.ManyToManyField(related_name='mactor_expertos_set', verbose_name=b'Expertos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Estudio_Mactor',
                'verbose_name_plural': 'Estudios_Mactor',
            },
        ),
        migrations.CreateModel(
            name='Informe_Final',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.IntegerField()),
                ('fecha', models.DateField(auto_now=True)),
                ('informe', models.TextField()),
                ('codigo_Estudio', models.PositiveIntegerField(default=1)),
                ('creador', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('cuestiones', models.ForeignKey(blank=True, to='mactor.Cuestion_Estrategica', null=True)),
            ],
            options={
                'verbose_name': 'Informe_final',
                'verbose_name_plural': 'Informes_finales',
            },
        ),
        migrations.CreateModel(
            name='Objetivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreLargo', models.CharField(max_length=50)),
                ('nombreCorto', models.CharField(max_length=10)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('codigo_Estudio', models.PositiveIntegerField(default=1)),
                ('creador', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Objetivo',
                'verbose_name_plural': 'Objetivos',
            },
        ),
        migrations.CreateModel(
            name='Relacion_Influencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.IntegerField(null=True, blank=True)),
                ('valor', models.IntegerField()),
                ('justificacion', models.TextField(null=True, blank=True)),
                ('codigo_Estudio', models.PositiveIntegerField(default=1)),
                ('actorX', models.ForeignKey(related_name='mactor_actorX_set', to='mactor.Actor', null=True)),
                ('actorY', models.ForeignKey(related_name='mactor_actorY_set', to='mactor.Actor', null=True)),
                ('creador', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Relacion_de_Influencia',
                'verbose_name_plural': 'Relaciones_de_influencia',
            },
        ),
        migrations.CreateModel(
            name='Relacion_MAO',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.IntegerField()),
                ('valor', models.IntegerField()),
                ('justificacion', models.TextField(max_length=50, null=True, blank=True)),
                ('codigo_Estudio', models.PositiveIntegerField(default=1)),
                ('actorY', models.ForeignKey(to='mactor.Actor')),
                ('creador', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('objetivoX', models.ForeignKey(to='mactor.Objetivo')),
            ],
            options={
                'verbose_name': 'Relacion_MAO',
                'verbose_name_plural': 'Relaciones_MAO',
            },
        ),
        migrations.AlterUniqueTogether(
            name='relacion_influencia',
            unique_together=set([('actorX', 'actorY')]),
        ),
    ]
