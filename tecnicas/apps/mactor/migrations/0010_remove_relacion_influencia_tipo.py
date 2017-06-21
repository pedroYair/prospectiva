# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0009_auto_20170604_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relacion_influencia',
            name='tipo',
        ),
    ]
