"""
Cache helper functions
"""

from django.contrib.auth.models import Permission
from django.contrib.sessions.models import Session
from django.core.cache import cache
from app.models import *


def get_permission():
	permission = cache.get('permission')
	if permission == None:
		permission = Permission.objects.get(name='Can change user')

		cache.set('permission', permission, settings.PERMISSION_CACHE_INTERVAL)

	return permission

def get_session_count():
	session_count = cache.get('session_count')
	if session_count == None:
		session_count = Session.objects.count()
		cache.set('session_count', session_count, settings.SESSION_CACHE_INTERVAL)
	return session_count


################################################################################

def get_user_list():
	user_list = cache.get('user_list')
	if user_list == None:
		user_list = User.objects.select_related().all()
		cache.set('user_list', user_list, settings.USER_LIST_CACHE_INTERVAL)
	return user_list

def get_user_object(id=None):

       user_obj = None
       user_list = get_user_list()
       try:
               user_obj = [l for l in user_list if l.id==int(id)]
               if user_obj == [] or user_obj == None:
                       user_obj = user_list.get(id=id)
               else:
                       user_obj = user_obj[0]
       except AttributeError:
               user_list = User.objects.select_related().all()
               cache.set('user_list', user_list, settings.USER_LIST_CACHE_INTERVAL)
               user_obj = get_user_object(id=id)
       return user_obj

################################################################################

def filter_quizchoiceselected_list(Quiz=None, User=None):
	if Quiz == None or User == None:
		return []
	key = 'Quizchoiceselected_%s_%s' % (Quiz.id, User.id)
	quizchoiceselected_list = cache.get(key)
	if quizchoiceselected_list == None:
		quizchoiceselected_list = Quizchoiceselected.objects.filter(Quiz=Quiz, User=User)
		cache.set(key, quizchoiceselected_list, settings.QUIZCHOICESELECTED_LIST_CACHE_INTERVAL)
	return quizchoiceselected_list

################################################################################

def filter_quizchoice_list(Quiz=None):
	if Quiz == None:
		return []
	key = 'Quizchoice_%s' % (Quiz.id)
	quizchoice_list = cache.get(key)
	if quizchoice_list == None:
		quizchoice_list = QuizChoice.objects.filter(Quiz=Quiz)

		cache.set(key, quizchoice_list, settings.QUIZCHOICE_LIST_CACHE_INTERVAL)
	return quizchoice_list

def filter_quizchoice_list_for_correct(Quiz=None, correct=None):
	if Quiz == None:
		return []
	key = 'Quizchoice_%s' % (Quiz.id)
	quizchoice_list = filter_quizchoice_list(Quiz=Quiz)
	try:
		filtered_quizchoice_list = [l for l in quizchoice_list if l.correct==correct]
		
	except AttributeError:
		quizchoice_list = QuizChoice.objects.select_related().all()
		cache.set('quizchoice_list', quizchoice_list, settings.QUIZCHOICE_LIST_CACHE_INTERVAL)
		filtered_quizchoice_list = quizchoice_list.filter(Quiz=Quiz)
	return filtered_quizchoice_list


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
	index = len(lecture_list)-1
	if index < 0:
		#return None if there are no Lectures
		return None
	try:
		lecture_obj = lecture_list[index]
	except AttributeError:
		lecture_list = Lecture.objects.select_related().all()
		cache.set('lecture_list', lecture_list, settings.LECTURE_LIST_CACHE_INTERVAL)
		lecture_obj = lecture_list[index]
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
		thread_list = Thread.objects.select_related().all()
		cache.set('thread_list', thread_list, settings.THREAD_LIST_CACHE_INTERVAL)
		thread_obj = [l for l in thread_list if l.id==int(id)]
		if thread_obj == [] or thread_obj == None:
			thread_obj = thread_list.get(id=id)
		else:
			thread_obj = thread_obj[0]
	return thread_obj

################################################################################

def get_post_list():
    post_list = cache.get('post_list')
    if post_list == None:
        post_list = Post.objects.select_related().all()
        cache.set('post_list', post_list, settings.POST_LIST_CACHE_INTERVAL)
    return post_list

def filter_post_list(Thread=None):
       kwargs = {}
       if Thread != None:
               kwargs.update({'Thread':Thread})
       filtered_post_list = None
       post_list = get_post_list()
       try:
               filtered_post_list = [l for l in post_list if l.Thread==Thread]
               
       except AttributeError:
               post_list = Post.objects.select_related().all()
               cache.set('post_list', post_list, settings.POST_LIST_CACHE_INTERVAL)
               filtered_post_list = post_list.filter(**kwargs)
       return filtered_post_list

def get_post_object(id=None):

       post_obj = None
       post_list = get_post_list()
       try:
               post_obj = [l for l in post_list if l.id==int(id)]
               if post_obj == [] or post_obj == None:
                       post_obj = post_list.get(id=id)
               else:
                       post_obj = post_obj[0]
       except AttributeError:
               post_list = Post.objects.select_related().all()
               cache.set('post_list', post_list, settings.POST_LIST_CACHE_INTERVAL)
               post_obj = [l for l in post_list if l.id==int(id)]
               if post_obj == [] or post_obj == None:
                       post_obj = post_list.get(id=id)
               else:
                       post_obj = post_obj[0]
       return post_obj