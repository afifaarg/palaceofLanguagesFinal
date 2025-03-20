# views.py
from django.http import HttpResponseRedirect
from django.utils.translation import activate
from django.conf import settings

def set_language(request, language_code):
    # Activate the selected language
    activate(language_code)

    # Store the selected language in the session
    request.session[settings.LANGUAGE_SESSION_KEY] = language_code

    # Redirect to the same page or a specific page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))