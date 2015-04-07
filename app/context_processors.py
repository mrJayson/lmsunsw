from app.models import ConfidenceMeter
from django.contrib.sessions.models import Session

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