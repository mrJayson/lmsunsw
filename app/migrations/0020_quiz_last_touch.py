# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20150420_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='last_touch',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 21, 12, 51, 40, 768720, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
