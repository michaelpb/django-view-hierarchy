from django.urls import reverse
from django.views import View

from django_view_hierarchy.utils import (
    get_info_from_cbv_instance,
    set_request_breadcrumbs,
)

class BreadcrumbMixin:
    breadcrumb = None
    view_name = None

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
        set_request_breadcrumbs(self.request, self.args, self.kwargs)

        # Finally, append current breadcrumb
        title, url = get_info_from_cbv_instance(self)
        self.request.breadcrumbs.append(title, url)
        return super().dispatch(*args, **kwargs)
