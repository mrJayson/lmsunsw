# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20150426_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wordcloud',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False),
            preserve_default=False,
        ),
    ]
