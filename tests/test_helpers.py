#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_helpers
------------

Tests for `django_view_hierarchy` helper functions and classes.
"""
from unittest.mock import MagicMock

from django.test import SimpleTestCase

from django_view_hierarchy import helpers

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


class TestGenerateBreadcrumbHierarchy(SimpleTestCase):
    def test_empty_hierarchy(self):
        results = helpers._generate_breadcrumb_hierarchy({})
        self.assertEqual(results, {})

    def test_single_flat_hierarchy(self):
        # Test a few properties of a flat hierarchy
        request = MagicMock()
        request.was_called = False
        def fake_view(request):
            self.assertTrue(hasattr(request, 'breadcrumbs'))
            # Breadcrumbs length should be 0
            self.assertEqual(request.breadcrumbs.breadcrumbs, [])
            self.assertEqual(request.breadcrumbs.bc_sources, [])
            request.was_called = True

        FakeCBV = MagicMock()
        FakeCBV.as_view.return_value = fake_view

        results = helpers._generate_breadcrumb_hierarchy({
            'a': FakeCBV,
        })
        self.assertEqual(set(results.keys()), set('a'))
        self.assertTrue(hasattr(results['a'], '__call__'))
        self.assertFalse(request.was_called)
        results['a'](request)
        self.assertTrue(request.was_called)

    def test_layered_hierarchy(self):
        request = MagicMock()
        request.was_called = False
        def fake_view(request):
            self.assertTrue(hasattr(request, 'breadcrumbs'))
            # Breadcrumbs length should be 0
            self.assertEqual(len(request.breadcrumbs.breadcrumbs), 0)
            # But sources length should be 2
            sources = request.breadcrumbs.bc_sources
            self.assertEqual(len(sources), 2)

            # Ensure that there are no parameters for any breadcrumbs
            args_set = set(args for view, args in sources)
            self.assertEqual(args_set, set([tuple()]))
            request.was_called = True

        FakeCBV = MagicMock()
        FakeCBV.as_view.return_value = fake_view

        results = helpers._generate_breadcrumb_hierarchy({
            'a': {
                '': MagicMock(),
                'b': {
                    '': MagicMock(),
                    'c': FakeCBV,
                },
            },
        })
        self.assertEqual(set(results.keys()), set('a'))
        self.assertFalse(request.was_called)
        results['a']['b']['c'](request)
        self.assertTrue(request.was_called)

    def test_layered_hierarchy_with_parameters(self):
        request = MagicMock()
        request.was_called = False
        def fake_view(request):
            # Ensure that there are 1 and 2 params for breadcrumbs
            sources = request.breadcrumbs.bc_sources
            self.assertEqual([count for view, count in sources],
                [('g', ), ('g', 'pk')])
            request.was_called = True

        FakeCBV = MagicMock()
        FakeCBV.as_view.return_value = fake_view
        results = helpers._generate_breadcrumb_hierarchy({
            r'u-(?P<g>\d+)': {
                '': MagicMock(),
                r'(?P<pk>\d+)': {
                    '': MagicMock(),
                    'activity': FakeCBV,
                },
            },
        })
        self.assertFalse(request.was_called)
        results[r'u-(?P<g>\d+)'][r'(?P<pk>\d+)']['activity'](request)
        self.assertTrue(request.was_called)

