# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150402_0133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizchoiceselected',
            old_name='quiz_choice',
            new_name='QuizChoice',
        ),
        migrations.RenameField(
            model_name='quizchoiceselected',
            old_name='user',
            new_name='User',
        ),
    ]
