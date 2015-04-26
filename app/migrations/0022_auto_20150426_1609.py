# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20150424_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='lecture_slide',
            field=models.FileField(help_text='Optional, Provide a URL link to the lecture slides to be displayed', null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
