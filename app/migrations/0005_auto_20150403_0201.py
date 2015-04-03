# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150402_1403'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='quizchoiceselected',
            unique_together=set([('User', 'QuizChoice')]),
        ),
    ]
