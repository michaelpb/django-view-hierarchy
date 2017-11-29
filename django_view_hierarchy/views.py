from django.urls import reverse

from django_view_hierarchy.utils import set_request_breadcrumbs


class BreadcrumbMixin:
    breadcrumb = None
    view_name = None
    breadcrumb_groups = None

    def get_reverse_url(self):
        return reverse(self.view_name, args=self.args, kwargs=self.kwargs)

    def get_breadcrumb(self):
        if self.breadcrumb:
            return self.breadcrumb

        if hasattr(self, 'get_object'):
            obj = self.get_object()
            return str(obj)
        return str(self.__name__)  # Default to name of this view

    def dispatch(self, *args, **kwargs):
        # Set up previous breadcrumbs
        set_request_breadcrumbs(self, self.request, self.args, self.kwargs)
        return super().dispatch(*args, **kwargs)
