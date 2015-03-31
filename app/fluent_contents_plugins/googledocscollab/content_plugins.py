"""
Plugin to add an ``<googledocscollab>`` to the page.
"""
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from fluent_contents.extensions import ContentPlugin, plugin_pool
from app.fluent_contents_plugins.googledocscollab.models import GoogleDocsCollabItem


@plugin_pool.register
class GoogleDocsCollabPlugin(ContentPlugin):
    model = GoogleDocsCollabItem
    category = _('Advanced')


    def render(self, request, instance, **kwargs):
        return mark_safe(u'<object data="{src}" width="{width}" height="{height}"></object>'.format(
            src=escape(instance.src),
            width=instance.width,
            height=instance.height
        ))
