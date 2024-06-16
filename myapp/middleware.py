# import datetime
# from django.utils import timezone
# from django.shortcuts import redirect
# from django.contrib import messages
# from django.conf import settings
# from django.contrib.auth import logout

# class SessionTimeoutMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             now = timezone.now()
#             last_activity = request.session.get('last_activity')

#             if last_activity:
#                 elapsed_time = (now - datetime.datetime.fromisoformat(last_activity)).total_seconds()
#                 if elapsed_time > settings.SESSION_COOKIE_AGE:
#                     logout(request)  # Log out the user
#                     messages.warning(request, 'Session time up! Please log in again.')
#                     return redirect('login')

#             request.session['last_activity'] = now.isoformat()

#         response = self.get_response(request)
#         return response

import datetime

from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponseRedirect
from django.urls import reverse


class SessionTimeoutMiddleware(SessionMiddleware):
    def process_request(self, request):
        if request.user.is_authenticated:
            current_time = datetime.datetime.now()
            if 'last_activity' in request.session:
                last_activity_str = request.session['last_activity']
                last_activity = datetime.datetime.fromisoformat(last_activity_str)  # Convert string to datetime
                if (current_time - last_activity).seconds > settings.SESSION_COOKIE_AGE:
                    request.session.flush()
                    return HttpResponseRedirect(reverse('login') + '?session_expired=True')
            request.session['last_activity'] = current_time.isoformat()  # Convert datetime to string
        return None