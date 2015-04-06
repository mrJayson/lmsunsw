# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20150406_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confidencemeter',
            name='User',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
