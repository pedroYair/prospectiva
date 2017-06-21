# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0005_auto_20170509_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='informacion',
        ),
    ]
