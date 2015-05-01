# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20150427_1720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordcloud',
            name='Lecture',
        ),
        migrations.AlterUniqueTogether(
            name='wordcloudsubmission',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='wordcloudsubmission',
            name='User',
        ),
        migrations.RemoveField(
            model_name='wordcloudsubmission',
            name='Wordcloud',
        ),
        migrations.DeleteModel(
            name='Wordcloud',
        ),
        migrations.DeleteModel(
            name='WordcloudSubmission',
        ),
    ]
