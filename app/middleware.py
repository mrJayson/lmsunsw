# custom middleware to apply to all views and requests

from session_security import middleware
from datetime import datetime, timedelta
from session_security.utils import get_last_activity, set_last_activity
from session_security.settings import EXPIRE_AFTER, PASSIVE_URLS
from django.contrib.auth import logout

def django_sessions(request):
	# context processor to add num of users on the site
	sessions_decoded_data = [i.get_decoded() for i in Session.objects.all()]
	users = []
	for data in sessions_decoded_data:
		if data.has_key('_auth_user_id'):
			users += [data.get('_auth_user_id')]
	num_sessions = len(set(users))
	ret_val = {'num_sessions':num_sessions}
	return ret_val

def get_confidence_meter_values(request):
	# context processor for retreiving data for confidence meter
	good = 0
	neutral = 0
	bad = 0
	for vote in ConfidenceMeter.objects.all():
		if vote.confidence == 1:
			good += 1
		elif vote.confidence == -1:
			bad += 1
		else:
			neutral += 1
	good = good * 100 / len(ConfidenceMeter.objects.all())
	neutral = neutral * 100 / len(ConfidenceMeter.objects.all())
	bad = bad * 100 / len(ConfidenceMeter.objects.all())
	if request.user.is_authenticated():
		try:
			current = ConfidenceMeter.objects.get(User=request.user).confidence
		except ConfidenceMeter.DoesNotExist:
			current = None
	else:
		current = None

	ret_val = {'good': good, 'neutral': neutral, 'bad': bad, 'current': current}
	return ret_val


class SessionSecurityMiddleware(middleware.SessionSecurityMiddleware):

	def process_request(self, request):

		#need to add session db delete line to maintain correct session entries in db
		""" Update last activity time or logout. """
		if not request.user.is_authenticated():
		    return

		now = datetime.now()
		self.update_last_activity(request, now)

		delta = now - get_last_activity(request.session)
		if delta >= timedelta(seconds=EXPIRE_AFTER):
			logout(request)
			Session.objects.all().get(session_key=request.session.session_key).delete()
			for session in Session.objects.all():
				if session.get_decoded().get('_auth_user_id') == request.user.id:
					# sometimes there are multiple sessions for the same user, delete those sessions as well
					session.delete()
		elif request.path not in PASSIVE_URLS:
		    set_last_activity(request.session, now)

