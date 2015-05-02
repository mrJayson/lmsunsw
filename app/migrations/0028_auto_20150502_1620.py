# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_quiz_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizchoiceselected',
            name='Quiz',
            field=models.ForeignKey(blank=True, to='app.Quiz', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quizchoiceselected',
            name='answer',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizchoiceselected',
            name='QuizChoice',
            field=models.ForeignKey(blank=True, to='app.QuizChoice', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='quizchoiceselected',
            unique_together=set([]),
        ),
    ]
