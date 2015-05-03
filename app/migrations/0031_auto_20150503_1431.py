# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_auto_20150503_0824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codesnippet',
            name='style',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='style',
        ),
    ]
