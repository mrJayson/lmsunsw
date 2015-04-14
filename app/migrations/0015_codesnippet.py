# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_thread_last_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeSnippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('syntax', models.CharField(max_length=30)),
                ('code', models.TextField()),
                ('linenumbers', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Code snippet',
                'verbose_name_plural': 'Code snippets',
            },
            bases=(models.Model,),
        ),
    ]
