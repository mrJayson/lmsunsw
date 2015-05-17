# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_userprofile_seat_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='seat_location',
            field=models.SmallIntegerField(default=1),
            preserve_default=True,
        ),
    ]
