from django import template
from wagtail.models import Locale
from django.utils.translation import get_language
register = template.Library()

@register.simple_tag(takes_context=True)
def get_available_languages(context, page):
    request = context['request']
    current_language = get_language()
    locales = Locale.objects.all()
    translated_pages = {}

    for locale in locales:
        translated_page = page.get_translation_or_none(locale)
        if translated_page:
            # Construct the URL manually instead of modifying the `url` property
            translated_url = f"/{locale.language_code}{translated_page.url}"
            translated_pages[locale.language_code] = {
                'page': translated_page,
                'url': translated_url,
            }

    # Add the current language to the context
    translated_pages['current_language'] = current_language

    return translated_pages

@register.simple_tag
def get_all_locales():
    return Locale.objects.all()

@register.filter
def dict_get(dictionary, key):
    """Custom filter to get a value from a dictionary in a Django template."""
    return dictionary.get(key, None)
