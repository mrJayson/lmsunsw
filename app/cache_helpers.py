"""
Cache helper functions
"""

from django.core.cache import cache
from app.models import *

def get_thread_list():
    thread_list = cache.get('thread_list')
    if thread_list == None:
        thread_list = Thread.objects.select_related().all()
        cache.set('thread_list', thread_list, settings.THREAD_LIST_CACHE_INTERVAL)
    return thread_list