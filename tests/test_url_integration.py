from django.test import Client
from django.test import TestCase, override_settings
from django.test import SimpleTestCase

# from django.views.generic import ListView
from django.views import View

from django.http import HttpResponse

from django_view_hierarchy import helpers
from django_view_hierarchy.views import BreadcrumbMixin
from django_view_hierarchy.decorators import breadcrumb

# Non-generic CBV
class UserListView(BreadcrumbMixin, View):
    breadcrumb = 'Users'

    def get(self, request):
        bc_str = ' '.join(str(bc) for bc in request.breadcrumbs)
        return HttpResponse('%s | User list view' % bc_str)

class UserDetailView(BreadcrumbMixin, View):
    breadcrumb = None
    # view_name = 'user_details'

    def get_breadcrumb(self):
        pk = self.kwargs['pk']
        return 'u%i' % int(pk)

    def get(self, request, pk):
        bc_str = ' '.join(str(bc) for bc in request.breadcrumbs)
        return HttpResponse('%s | User_%i detail view' % (bc_str, int(pk)))

class UserActivityDetailView(BreadcrumbMixin, View):
    breadcrumb = 'Activity'

    def get(self, request, pk):
        bc_str = ' '.join(str(bc) for bc in request.breadcrumbs)
        return HttpResponse('%s | User_%i activity' % (bc_str, int(pk)))

@breadcrumb('Followers')
def user_followers_view(request, pk):
    bc_str = ' '.join(str(bc) for bc in request.breadcrumbs)
    return HttpResponse('%s | User_%i followers' % (bc_str, int(pk)))

@breadcrumb('Projects')
def project_list_view(request):
    bc_str = ' '.join(str(bc) for bc in request.breadcrumbs)
    return HttpResponse('%s | Project list view' % bc_str)

@breadcrumb(lambda request, pk: 'p%i' % int(pk))
def project_detail_view(request, pk):
    bc_str = ' '.join(str(bc) for bc in request.breadcrumbs)
    return HttpResponse('%s | Project_%i details' % (bc_str, int(pk)))

@breadcrumb('Pactivity')
def project_activity_view(request, pk):
    bc_str = ' '.join(str(bc) for bc in request.breadcrumbs)
    return HttpResponse('%s | Project_%i activity' % (bc_str, int(pk)))

class ForkDetailView(BreadcrumbMixin, View):
    breadcrumb = 'Forks'

    def get(self, request, pk):
        bc_str = ' '.join(str(bc) for bc in request.breadcrumbs)
        return HttpResponse('%s | Project_%i forks' % (bc_str, int(pk)))

TEST_BREADCRUMB_HIERARCHY = {
    # Class based views
    'users': {
        '': UserListView,
        '(?P<pk>\d+)': {
            '': UserDetailView,
            'activity': UserActivityDetailView,
            'followers': user_followers_view, # mixed flat and CBV
        },
    },

    # Do flat views
    'projects': {
        '': project_list_view,
        '(?P<pk>\d+)': {
            '': project_detail_view,
            'activity': project_activity_view,
            'forks': ForkDetailView,  # Mixed flat and CBV
        },
    },
}

urlpatterns = helpers.view_hierarchy(TEST_BREADCRUMB_HIERARCHY)

@override_settings(ROOT_URLCONF=__name__)
class TestCBVRoutes(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_view_routes(self):
        # Tests that the GET routes are all set up as expected
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User list view', response.content)

        response = self.client.get('/users/5/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User_5 detail view', response.content)

        response = self.client.get('/users/5/activity/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User_5 activity', response.content)

    def test_rendered_breadcrumbs(self):
        paths = ['/users/', '/users/2/', '/users/2/activity/']

        # Check all paths for initial breadcrumb
        for path in paths:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            bc = b'<a href="/users/">Users</a>'
            self.assertIn(bc, response.content)

        # Check last two paths for final breadcrumb
        for path in paths[1:]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            bc = b'<a href="/users/2/">u2</a>'
            self.assertIn(bc, response.content)

        # Check final path for final breadcrumb
        path = paths[2]
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        bc = b'<a href="/users/2/activity/">Activity</a>'
        self.assertIn(bc, response.content)


@override_settings(ROOT_URLCONF=__name__)
class TestFunctionalViewRoutes(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_view_routes(self):
        # Tests that the GET routes are all set up as expected
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project list view', response.content)

        response = self.client.get('/projects/555/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project_555 detail', response.content)

        response = self.client.get('/projects/555/activity/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project_555 activity', response.content)


    def test_rendered_breadcrumbs_for_flat_views(self):
        paths = ['/projects/', '/projects/2/', '/projects/2/activity/']

        # Check all paths for initial breadcrumb
        for path in paths:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            bc = b'<a href="/projects/">Projects</a>'
            self.assertIn(bc, response.content)

        # Check last two paths for final breadcrumb
        for path in paths[1:]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            bc = b'<a href="/projects/2/">p2</a>'
            self.assertIn(bc, response.content)

        # Check final path for final breadcrumb
        path = paths[2]
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        bc = b'<a href="/projects/2/activity/">Pactivity</a>'
        self.assertIn(bc, response.content)


@override_settings(ROOT_URLCONF=__name__)
class TestMixedRoutes(SimpleTestCase):
    def test_cbv_inheriting_func(self):
        # Check final path for all breadcrumbs and text breadcrumb
        response = self.client.get('/projects/123/forks/')
        self.assertEqual(response.status_code, 200)
        c = response.content

        # Check text
        self.assertIn(b'Project_123 forks', c)

        # Check breadcrumbs
        self.assertIn(b'<a href="/projects/">Projects</a>', response.content)
        self.assertIn(b'<a href="/projects/123/">p123</a>', c)
        self.assertIn(b'<a href="/projects/123/forks/">Forks</a>', c)


    def test_functional_child_of_cbv(self):
        # Check final path for final breadcrumb
        response = self.client.get('/users/2/followers/')
        self.assertEqual(response.status_code, 200)

        # Check breadcrumbs
        c = response.content
        self.assertIn(b'User_2 followers', c)
        self.assertIn(b'<a href="/users/">Users</a>', c)
        self.assertIn(b'<a href="/users/2/">u2</a>', c)
        self.assertIn(b'<a href="/users/2/followers/">Followers</a>', c)

