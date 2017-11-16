#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_helpers
------------

Tests for `django_view_hierarchy` helper functions and classes.
"""
from django.test import SimpleTestCase

from django_view_hierarchy import helpers

from django.views.generic import ListView
from django.views import View

# Some helper functions
def user_list(request): pass
def post_list(request): pass
def user_view(request, uid): pass
def user_view_activity(request, uid): pass

TEST_HIERARCHY = {
    'users/': {
        '': user_list,
        '(?P<uid>\d+)': {
            '': user_view,
            'activity': user_view_activity,
        },
    },
    'posts': post_list,
}

from django.views import View

class UserListView(View):
    breadcrumb = 'User'

class UserDetailView(View):
    breadcrumb = None

    def get_breadcrumb(self):
        return 'User Name'

class UserActivityDetailView(UserDetailView):
    breadcrumb = 'Activity'

TEST_BREADCRUMB_HIERARCHY = {
    'users': {
        '': UserListView,
        '(?P<pk>\d+)': {
            '': UserDetailView,
            'activity': UserActivityDetailView,
        },
    },
}


class TestFlattenHierarchy(SimpleTestCase):
    def test_empty_hierarchy(self):
        self.assertEqual(helpers._flatten_hierarchy({}), [])

    def test_singular_path(self):
        self.assertEqual(helpers._flatten_hierarchy({
            'users': user_list,
        }), [('^users/$', user_list)])

        self.assertEqual(helpers._flatten_hierarchy({
            '': user_list,
        }), [('^$', user_list)])

    def test_multiple_paths(self):
        self.assertEqual(helpers._flatten_hierarchy({
            'posts': post_list,
            'users': user_list,
        }), [
            ('^posts/$', post_list),
            ('^users/$', user_list),
        ])

    def test_multiple_paths_alphabetical(self):
        self.assertEqual(helpers._flatten_hierarchy({
            'd': post_list,
            'b': user_list,
            'a': post_list,
            'c': user_list,
        }), [
            ('^a/$', post_list),
            ('^b/$', user_list),
            ('^c/$', user_list),
            ('^d/$', post_list),
        ])

    def test_hierarchy(self):
        self.assertEqual(helpers._flatten_hierarchy(TEST_HIERARCHY), [
            (r'^posts/$', post_list),
            (r'^users/$', user_list),
            (r'^users/(?P<uid>\d+)/$', user_view),
            (r'^users/(?P<uid>\d+)/activity/$', user_view_activity),
        ])


