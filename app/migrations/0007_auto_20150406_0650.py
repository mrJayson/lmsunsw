# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_confidencemeter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confidencemeter',
            name='confidence',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
