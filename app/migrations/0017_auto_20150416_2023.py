# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0016_codesnippet_style'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wordcloud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=30)),
                ('image', models.ImageField(null=True, upload_to=b'wordcloud', blank=True)),
                ('visible', models.BooleanField(default=False)),
                ('Lecture', models.ForeignKey(to='app.Lecture')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordcloudSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=30)),
                ('User', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('Wordcloud', models.ForeignKey(to='app.Wordcloud')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='wordcloudsubmission',
            unique_together=set([('User', 'Wordcloud')]),
        ),
    ]
