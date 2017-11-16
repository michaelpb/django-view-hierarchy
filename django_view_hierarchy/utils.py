import json

from django.contrib.contenttypes.models import ContentType


def get_gfk(instance):
    '''
    Given a model instance, returns a dictionary of the content_type and
    object_id to allow for easy searching
    '''
    content_type = ContentType.objects.get_for_model(instance)
    return {
        'content_type': content_type,
        'object_id': instance.id,
    }


def parse_json_list(json_iterable):
    '''
    Given an iterable containing dicts with cached_json and dates, parse the
    JSON and flatten each into a single dict.
    '''
    return [
        dict(
            date=item['date'],
            **(json.loads(item['cached_json']) if item['cached_json'] else {})
        )
        for item in json_iterable
    ]


class HtmlWrapper(dict):
    def __str__(self):
        return self['cached_html']


def parse_html_list(html_list):
    '''
    Given an iterable containing dicts with HTML and dates, flatten into a dict
    that resolves to the HTML when treated like a string.
    '''
    return [HtmlWrapper(item) for item in html_list]
