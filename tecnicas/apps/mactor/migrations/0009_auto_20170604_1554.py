# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0008_auto_20170517_2015'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='relacion_influencia',
            unique_together=set([('actorX', 'actorY', 'creador')]),
        ),
    ]
