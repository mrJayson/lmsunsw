# custom middleware to apply to all views and requests

from session_security import middleware
from datetime import datetime, timedelta
from session_security.utils import get_last_activity, set_last_activity
from session_security.settings import EXPIRE_AFTER, PASSIVE_URLS
from django.contrib.auth import logout
from django.contrib.sessions.models import Session

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

