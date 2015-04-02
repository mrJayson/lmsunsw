# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150402_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='collab_doc',
            field=models.URLField(help_text=b'Optional, Provide a URL Link to a specific google docs, a blank default will be used if empty', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='lecture_slide',
            field=models.URLField(help_text=b'Optional, Provide a URL link to the lecture slides to be displayed', null=True, blank=True),
            preserve_default=True,
        ),
    ]
