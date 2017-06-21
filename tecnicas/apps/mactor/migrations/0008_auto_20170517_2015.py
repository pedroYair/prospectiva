# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0007_auto_20170517_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relacion_influencia',
            name='actorY',
            field=models.ForeignKey(related_name='mactor_actorY_set', to='mactor.Actor', null=True),
        ),
    ]
