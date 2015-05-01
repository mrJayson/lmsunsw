# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20150501_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='code',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='linenumbers',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='style',
            field=models.CharField(default=b'default', max_length=30, null=True, blank=True, choices=[(b'manni', b'manni::ManniStyle'), (b'igor', b'igor::IgorStyle'), (b'xcode', b'xcode::XcodeStyle'), (b'vim', b'vim::VimStyle'), (b'autumn', b'autumn::AutumnStyle'), (b'vs', b'vs::VisualStudioStyle'), (b'rrt', b'rrt::RrtStyle'), (b'native', b'native::NativeStyle'), (b'perldoc', b'perldoc::PerldocStyle'), (b'borland', b'borland::BorlandStyle'), (b'tango', b'tango::TangoStyle'), (b'emacs', b'emacs::EmacsStyle'), (b'friendly', b'friendly::FriendlyStyle'), (b'monokai', b'monokai::MonokaiStyle'), (b'paraiso-dark', b'paraiso_dark::ParaisoDarkStyle'), (b'colorful', b'colorful::ColorfulStyle'), (b'murphy', b'murphy::MurphyStyle'), (b'bw', b'bw::BlackWhiteStyle'), (b'pastie', b'pastie::PastieStyle'), (b'paraiso-light', b'paraiso_light::ParaisoLightStyle'), (b'trac', b'trac::TracStyle'), (b'default', b'default::DefaultStyle'), (b'fruity', b'fruity::FruityStyle')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='syntax',
            field=models.CharField(default=b'html', max_length=30, null=True, blank=True, choices=[(b'as3', b'as3'), (b'bash', b'bash'), (b'c', b'c'), (b'cpp', b'cpp'), (b'csharp', b'csharp'), (b'css', b'css'), (b'html', b'html'), (b'java', b'java'), (b'js', b'js'), (b'make', b'make'), (b'objective-c', b'objective-c'), (b'perl', b'perl'), (b'php', b'php'), (b'python', b'python'), (b'sql', b'sql'), (b'ruby', b'ruby'), (b'vb.net', b'vb.net'), (b'xml', b'xml'), (b'xslt', b'xslt')]),
            preserve_default=True,
        ),
    ]
