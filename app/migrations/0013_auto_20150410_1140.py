# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_wordcloud'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quizproxy',
            options={'verbose_name': 'Quiz Result', 'verbose_name_plural': 'Quiz Results'},
        ),
        migrations.AddField(
            model_name='post',
            name='anonymous',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
