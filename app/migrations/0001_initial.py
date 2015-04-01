# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lecture_name', models.CharField(unique=True, max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField()),
                ('visible', models.BooleanField(default=False)),
                ('Lecture', models.ForeignKey(to='app.Lecture')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.TextField()),
                ('correct', models.BooleanField(default=False)),
                ('Quiz', models.ForeignKey(to='app.Quiz')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizChoiceSelected',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quiz_choice', models.ForeignKey(to='app.QuizChoice')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('app.quiz',),
        ),
    ]
