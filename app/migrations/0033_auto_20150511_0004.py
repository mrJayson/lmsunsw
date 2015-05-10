# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_thread_replies'),
    ]

    operations = [
        migrations.DeleteModel(
            name='QuizProxy',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='personal_collab_doc',
            field=models.URLField(help_text='Optional, Provide a URL Link to a specific google docs which will override the default public doc, you can share this with your friends to create small groups', null=True, blank=True),
            preserve_default=True,
        ),
    ]
