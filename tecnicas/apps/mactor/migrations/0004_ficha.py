# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0003_auto_20170420_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ficha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('objetivos', models.TextField(null=True, blank=True)),
                ('preferencias', models.TextField(null=True, blank=True)),
                ('motivaciones', models.TextField(null=True, blank=True)),
                ('propuestas', models.TextField(null=True, blank=True)),
                ('comportamiento', models.TextField(null=True, blank=True)),
                ('recursos', models.TextField(null=True, blank=True)),
                ('nombre', models.ForeignKey(to='mactor.Actor')),
            ],
            options={
                'verbose_name': 'Ficha',
                'verbose_name_plural': 'Fichas',
            },
        ),
    ]
