import re
from collections import namedtuple

from django.conf import settings
from django.contrib.auth.decorators import login_required

class Breadcrumb(namedtuple('Breadcrumb', ['title', 'url'])):
    def __str__(self):
        return '<a href="%s">%s</a>' % (
            self.url,
            self.title,
        )

class BreadcrumbList:
    def __init__(self):
        self.bc_sources = []

    def append(self, title, url):
        super().append(Breadcrumb(title, url))

    def add_breadcrumb_source(self, view, arg_count):
        self.bc_sources.append((view, arg_count))

class BreadcrumbsMiddleware(object):
    def process_request(self, request):
        request.breadcrumbs = BreadcrumbList()

