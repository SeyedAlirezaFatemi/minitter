from django.contrib.sessions.models import Session


class OneSessionPerUser:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            old_session_key = request.user.logged_in_user.session_key
            # Find the current session key
            current_session_key = request.session.session_key
            if old_session_key and old_session_key != current_session_key:
                # Delete the old session key if it exists
                try:
                    old_session = Session.objects.get(session_key=old_session_key)
                except Session.DoesNotExist:
                    pass
                else:
                    old_session.delete()

            request.user.logged_in_user.session_key = current_session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)
        return response
