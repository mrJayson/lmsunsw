# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_codesnippet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codesnippet',
            name='syntax',
            field=models.CharField(default=b'html', max_length=30, choices=[(b'as3', b'as3'), (b'bash', b'bash'), (b'c', b'c'), (b'cpp', b'cpp'), (b'csharp', b'csharp'), (b'css', b'css'), (b'html', b'html'), (b'java', b'java'), (b'js', b'js'), (b'make', b'make'), (b'objective-c', b'objective-c'), (b'perl', b'perl'), (b'php', b'php'), (b'python', b'python'), (b'sql', b'sql'), (b'ruby', b'ruby'), (b'vb.net', b'vb.net'), (b'xml', b'xml'), (b'xslt', b'xslt')]),
            preserve_default=True,
        ),
    ]
