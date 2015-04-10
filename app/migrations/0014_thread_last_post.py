# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20150410_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='last_post',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 10, 12, 2, 57, 676771), auto_now=True),
            preserve_default=False,
        ),
    ]
