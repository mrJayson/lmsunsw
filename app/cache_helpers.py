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
################################################################################
def get_quiz_list():
	quiz_list = cache.get('quiz_list')
	if quiz_list == None:
		quiz_list = Quiz.objects.select_related().all()
		cache.set('quiz_list', quiz_list, settings.QUIZ_LIST_CACHE_INTERVAL)
	return quiz_list

def get_quiz_object(id=None, visible=None, Lecture=None):
	kwargs = {}
	if id != None:
		kwargs.update({'id':id})
	if visible != None:
		kwargs.update({'visible':visible})
	if Lecture != None:
		kwargs.update({'Lecture':Lecture})
	quiz_obj = None
	quiz_list = get_quiz_list()
	try:
		if id!=None and visible==None and Lecture==None:
			quiz_obj = [l for l in quiz_list if l.id==int(id)]
		elif id==None and visible!=None and Lecture==None:
			quiz_obj = [l for l in quiz_list if l.visible==visible]
		elif id==None and visible==None and Lecture!=None:
			quiz_obj = [l for l in quiz_list if l.Lecture==Lecture]
		elif id!=None and visible!=None and Lecture==None:
			quiz_obj = [l for l in quiz_list if l.id==int(id) and l.visible==visible]
		elif id==None and visible!=None and Lecture!=None:
			quiz_obj = [l for l in quiz_list if l.visible==visible and l.Lecture==Lecture]
		elif id!=None and visible==None and Lecture!=None:
			quiz_obj = [l for l in quiz_list if l.id==int(id) and l.Lecture==Lecture]
		else:
			quiz_obj = quiz_list.get(**kwargs)

		if quiz_obj == [] or quiz_obj == None:
			quiz_obj = quiz_list.get(**kwargs)
		else:
			quiz_obj = quiz_obj[0]

	except AttributeError:
		quiz_list = Quiz.objects.select_related().all()
		cache.set('quiz_list', quiz_list, settings.QUIZ_LIST_CACHE_INTERVAL)
		quiz_obj = quiz_list.get(**kwargs)
	return quiz_obj

def filter_quiz_list(id=None, visible=None, Lecture=None):
	kwargs = {}
	if id != None:
		kwargs.update({'id':id})
	if visible != None:
		kwargs.update({'visible':visible})
	if Lecture != None:
		kwargs.update({'Lecture':Lecture})
	filtered_quiz_list = None
	quiz_list = get_quiz_list()
	try:

		if id!=None and visible==None and Lecture==None:
			filtered_quiz_list = [l for l in quiz_list if l.id==int(id)]
		elif id==None and visible!=None and Lecture==None:
			filtered_quiz_list = [l for l in quiz_list if l.visible==visible]
		elif id==None and visible==None and Lecture!=None:
			filtered_quiz_list = [l for l in quiz_list if l.Lecture==Lecture]
		elif id!=None and visible!=None and Lecture==None:
			filtered_quiz_list = [l for l in quiz_list if l.id==int(id) and l.visible==visible]
		elif id==None and visible!=None and Lecture!=None:
			filtered_quiz_list = [l for l in quiz_list if l.visible==visible and l.Lecture==Lecture]
		elif id!=None and visible==None and Lecture!=None:
			filtered_quiz_list = [l for l in quiz_list if l.id==int(id) and l.Lecture==Lecture]
		else:
			filtered_quiz_list = quiz_list.filter(**kwargs)
		
	except AttributeError:
		quiz_list = Quiz.objects.select_related().all()
		cache.set('quiz_list', quiz_list, settings.QUIZ_LIST_CACHE_INTERVAL)
		filtered_quiz_list = quiz_list.filter(**kwargs)
	return filtered_quiz_list
################################################################################
def get_lecture_list():
    lecture_list = cache.get('lecture_list')
    if lecture_list == None:
        lecture_list = Lecture.objects.select_related().all()
        cache.set('lecture_list', lecture_list, settings.LECTURE_LIST_CACHE_INTERVAL)
    return lecture_list

def get_lecture_object(id=None):

	lecture_obj = None
	lecture_list = get_lecture_list()
	try:
		lecture_obj = [l for l in lecture_list if l.id==int(id)]
		if lecture_obj == [] or lecture_obj == None:
			lecture_obj = lecture_list.get(id=id)
		else:
			lecture_obj = lecture_obj[0]
	except AttributeError:
		lecture_list = Lecture.objects.select_related().all()
		cache.set('lecture_list', lecture_list, settings.LECTURE_LIST_CACHE_INTERVAL)
		lecture_obj = [l for l in lecture_list if l.id==int(id)]
		if lecture_obj == [] or lecture_obj == None:
			lecture_obj = lecture_list.get(id=id)
		else:
			lecture_obj = lecture_obj[0]
	return lecture_obj

def get_last_lecture_object():
	lecture_obj = None
	lecture_list = get_lecture_list()
	try:
		lecture_obj = lecture_list[len(lecture_list)-1]
	except AttributeError:
		lecture_list = Lecture.objects.select_related().all()
		cache.set('lecture_list', lecture_list, settings.LECTURE_LIST_CACHE_INTERVAL)
		lecture_obj = lecture_list[len(lecture_list)-1]
	return lecture_obj
################################################################################

def get_codesnippet_list():
    codesnippet_list = cache.get('codesnippet_list')
    if codesnippet_list == None:
        codesnippet_list = CodeSnippet.objects.select_related().all()
        cache.set('codesnippet_list', codesnippet_list, settings.CODESNIPPET_LIST_CACHE_INTERVAL)
    return codesnippet_list

def filter_codesnippet_list(Lecture=None):
	kwargs = {}
	if Lecture != None:
		kwargs.update({'Lecture':Lecture})
	filtered_codesnippet_list = None
	codesnippet_list = get_codesnippet_list()
	try:
		filtered_codesnippet_list = [l for l in codesnippet_list if l.Lecture==Lecture]
		
	except AttributeError:
		codesnippet_list = CodeSnippet.objects.select_related().all()
		cache.set('codesnippet_list', codesnippet_list, settings.CODESNIPPET_LIST_CACHE_INTERVAL)
		filtered_codesnippet_list = codesnippet_list.filter(**kwargs)
	return filtered_codesnippet_list

################################################################################

def get_thread_list():
    thread_list = cache.get('thread_list')
    if thread_list == None:
        thread_list = Thread.objects.select_related().all()
        cache.set('thread_list', thread_list, settings.THREAD_LIST_CACHE_INTERVAL)
    return thread_list

def get_thread_object(id=None):

	thread_obj = None
	thread_list = get_thread_list()
	try:
		thread_obj = [l for l in thread_list if l.id==int(id)]
		if thread_obj == [] or thread_obj == None:
			thread_obj = thread_list.get(id=id)
		else:
			thread_obj = thread_obj[0]
	except AttributeError:
		thread_list = thread.objects.select_related().all()
		cache.set('thread_list', thread_list, settings.THREAD_LIST_CACHE_INTERVAL)
		thread_obj = [l for l in thread_list if l.id==int(id)]
		if thread_obj == [] or thread_obj == None:
			thread_obj = thread_list.get(id=id)
		else:
			thread_obj = thread_obj[0]
	return thread_obj
