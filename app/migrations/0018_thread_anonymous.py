# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20150416_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='anonymous',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
