# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20150414_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='codesnippet',
            name='style',
            field=models.CharField(default=b'default', max_length=30, choices=[(b'manni', b'manni::ManniStyle'), (b'igor', b'igor::IgorStyle'), (b'xcode', b'xcode::XcodeStyle'), (b'vim', b'vim::VimStyle'), (b'autumn', b'autumn::AutumnStyle'), (b'vs', b'vs::VisualStudioStyle'), (b'rrt', b'rrt::RrtStyle'), (b'native', b'native::NativeStyle'), (b'perldoc', b'perldoc::PerldocStyle'), (b'borland', b'borland::BorlandStyle'), (b'tango', b'tango::TangoStyle'), (b'emacs', b'emacs::EmacsStyle'), (b'friendly', b'friendly::FriendlyStyle'), (b'monokai', b'monokai::MonokaiStyle'), (b'paraiso-dark', b'paraiso_dark::ParaisoDarkStyle'), (b'colorful', b'colorful::ColorfulStyle'), (b'murphy', b'murphy::MurphyStyle'), (b'bw', b'bw::BlackWhiteStyle'), (b'pastie', b'pastie::PastieStyle'), (b'paraiso-light', b'paraiso_light::ParaisoLightStyle'), (b'trac', b'trac::TracStyle'), (b'default', b'default::DefaultStyle'), (b'fruity', b'fruity::FruityStyle')]),
            preserve_default=True,
        ),
    ]
