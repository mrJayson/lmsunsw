# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20150426_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='LectureMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('local_lecture_material', models.FileField(null=True, upload_to=b'lecture', blank=True)),
                ('online_lecture_material', models.URLField(null=True, blank=True)),
                ('Lecture', models.ForeignKey(to='app.Lecture')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='lecture',
            old_name='lecture_name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='lecture_slide',
        ),
    ]
