# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django_view_hierarchy.urls import urlpatterns as django_view_hierarchy_urls
from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include(django_view_hierarchy_urls, namespace='django_view_hierarchy')),
]
