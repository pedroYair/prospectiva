# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0004_ficha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='creador',
        ),
        migrations.RemoveField(
            model_name='objetivo',
            name='creador',
        ),
    ]
