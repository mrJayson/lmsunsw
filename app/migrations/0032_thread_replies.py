# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20150503_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='replies',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
