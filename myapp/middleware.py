import logging
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import logout
logger = logging.getLogger(__name__)
class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if True:
            if request.user.is_authenticated:
                current_time = timezone.now().timestamp()
                session_start_time = request.session.get('session_start_time', current_time)
                print('Start Time: ',session_start_time)
                print(current_time - session_start_time)
                if current_time - session_start_time > 15:  # Adjust the timeout as per your requirement
                    # Log the logout time
                    logger.info(f"User {request.user.username} logged out at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    from django.contrib.auth import logout
                    logout(request)
                    exit()
                else:
                    request.session['session_start_time'] = session_start_time

        response = self.get_response(request)
        return response
