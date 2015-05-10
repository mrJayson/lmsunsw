"""
Definition of custom context processors.
"""

from django.utils.translation import ugettext_lazy as _

from django.utils.text import capfirst
from django.db.models import get_models
from django.utils.safestring import mark_safe
from django.contrib.admin import ModelAdmin
from django.contrib.admin.validation import BaseValidator
from django.core.cache import cache
from django.conf import settings
from app.cache_helpers import *


from app.models import ConfidenceMeter, Quiz, Lecture, QuizChoice, QuizChoiceSelected


def django_sessions(request):
	# context processor to add num of users on the site
    session_count = get_session_count()
    ret_val = {'session_count':session_count}
    return ret_val

def prepare_confidence_meter_values(request):
    if not request.user.is_authenticated():
        return {}
    confidence_meter_data = get_confidence_meter_values(request)

    good_confidence_meter_data = confidence_meter_data['good_confidence_meter_data']
    neutral_confidence_meter_data = confidence_meter_data['neutral_confidence_meter_data']
    bad_confidence_meter_data = confidence_meter_data['bad_confidence_meter_data']

    sum = good_confidence_meter_data+neutral_confidence_meter_data+bad_confidence_meter_data
    sum = 1 if sum == 0 else sum
    good_confidence_meter_data = good_confidence_meter_data*100/sum
    neutral_confidence_meter_data = neutral_confidence_meter_data*100/sum
    bad_confidence_meter_data = bad_confidence_meter_data*100/sum
    confidence_meter_data.update({'good_confidence_meter_data': good_confidence_meter_data, 'neutral_confidence_meter_data': neutral_confidence_meter_data, 'bad_confidence_meter_data': bad_confidence_meter_data})

    return confidence_meter_data

def get_confidence_meter_values(request):
	# context processor for retrieving data for confidence meter

    # prevent unecessary processing if not authenticated, only authed pages can see
    if not request.user.is_authenticated():
        return {}

    confidence_meter_data = cache.get_many(['good_confidence_meter_data', 'neutral_confidence_meter_data', 'bad_confidence_meter_data'])

    if confidence_meter_data == {}:
        good_confidence_meter_data = 0
        neutral_confidence_meter_data = 0
        bad_confidence_meter_data = 0
        for vote in ConfidenceMeter.objects.select_related().all():
            if vote.confidence == 1:
                good_confidence_meter_data += 1
            elif vote.confidence == -1:
                bad_confidence_meter_data += 1
            else:
                neutral_confidence_meter_data += 1

        confidence_meter_data = {'good_confidence_meter_data': good_confidence_meter_data, 'neutral_confidence_meter_data': neutral_confidence_meter_data, 'bad_confidence_meter_data': bad_confidence_meter_data}
        # store in cache
        cache.set_many(confidence_meter_data, settings.STUDENT_POLL_INTERVAL)

    # get current vote if exists for display on web page
    confidence_meter_data.update({'current': get_user_confidence(request.user)})
    return confidence_meter_data

def currents(request):

    return {'current_quiz_list': filter_quiz_list(visible=True),
    'current_url': request.path,
    }

# get_models returns all the models, but there are 
# some which we would like to ignore
IGNORE_MODELS = (
    "sites",
    "sessions",
    "admin",
    "contenttypes",
)
IGNORE_APPS = (
	"ConfidenceMeter",
	"QuizChoice",
	"QuizChoiceSelected",
	"Post",
	"Permission",
	"Group",
    "LectureMaterial",
    "Thread",
)

# apps to ignore for students
IGNORE_APPS_FOR_STUDENTS = (
	"Thread",
	)



def app_list(request):
    '''
    Get all models and add them to the context apps variable.
    '''
    if not request.user.is_superuser:
        return {}
    user = request.user
    app_dict = {}
    admin_class = ModelAdmin
    for model in get_models():
        BaseValidator().validate(admin_class, model)
        model_admin = admin_class(model, None)
        app_label = model._meta.app_label
        if app_label in IGNORE_MODELS:
        	# skip rest of loop, start with next iteration
            continue
        if model.__name__ in IGNORE_APPS:
        	# skip rest of loop, start with next iteration
            continue
        if not user.is_superuser:
            if model.__name__ in IGNORE_APPS_FOR_STUDENTS:
        		# skip rest of loop, start with next iteration
                continue
        has_module_perms = user.has_module_perms(app_label)
        if has_module_perms:
            perms = model_admin.get_model_perms(request)
            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True in perms.values():
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'admin_url': mark_safe('/admin/%s/%s/' % (app_label, model.__name__.lower())),
                }
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    app_dict[app_label] = {
                        'name': app_label.title(),
                        'app_url': app_label + '/',
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                    }
    app_list = app_dict.values()
    app_list.sort(key=lambda x: x['name'])
    for app in app_list:
        app['models'].sort(key=lambda x: x['name'])
    return {'apps_list': app_list}