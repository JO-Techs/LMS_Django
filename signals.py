from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.utils.timezone import now

@receiver(user_logged_in)
def remove_other_sessions(sender, request, user, **kwargs):
    current_session_key = request.session.session_key
    user_sessions = Session.objects.filter(expire_date__gte=now())
    for session in user_sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(user.id):
            if session.session_key != current_session_key:
                session.delete()