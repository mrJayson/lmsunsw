# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20150407_2258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wordcloud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=30)),
                ('words', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(upload_to=b'wordcloud')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
