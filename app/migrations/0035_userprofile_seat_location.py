# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_userprofile_confidence_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='seat_location',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
