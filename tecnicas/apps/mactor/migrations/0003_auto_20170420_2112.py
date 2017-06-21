# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0002_auto_20170420_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudio_mactor',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='estudio_mactor',
            name='fecha_final',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='estudio_mactor',
            name='fecha_inicio',
            field=models.DateField(null=True, blank=True),
        ),
    ]
