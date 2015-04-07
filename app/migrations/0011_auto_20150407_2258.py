# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_thread_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thread',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False),
            preserve_default=False,
        ),
    ]
