# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudio_mactor',
            name='descripcion',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='estudio_mactor',
            name='titulo',
            field=models.CharField(max_length=200),
        ),
    ]
