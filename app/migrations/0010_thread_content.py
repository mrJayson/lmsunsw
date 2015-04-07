# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20150407_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
