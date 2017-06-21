# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0006_remove_actor_informacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relacion_influencia',
            name='actorY',
            field=models.ForeignKey(related_name='mactor_actorY_set', blank=True, to='mactor.Actor', null=True),
        ),
    ]
