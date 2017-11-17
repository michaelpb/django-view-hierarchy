from django.test import Client
from django.test import TestCase, override_settings
from django.test import SimpleTestCase

# from django.views.generic import ListView
from django.views import View

from django.http import HttpResponse

from django_view_hierarchy import helpers
from django_view_hierarchy.views import BreadcrumbMixin

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

TEST_BREADCRUMB_HIERARCHY = {
    'users': {
        '': UserListView,
        '(?P<pk>\d+)': {
            '': UserDetailView,
            'activity': UserActivityDetailView,
        },
    },
}

urlpatterns = helpers.view_hierarchy(TEST_BREADCRUMB_HIERARCHY)

@override_settings(ROOT_URLCONF=__name__)
class TestRoutes(SimpleTestCase):
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



