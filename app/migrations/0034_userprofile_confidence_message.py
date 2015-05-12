# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20150511_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='confidence_message',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
