from django.urls import reverse

def get_breadcrumb_info_from_view(view):
    url = view.get_reverse_url()
    if view.breadcrumb:
        return str(view.breadcrumb), url
    return view.get_breadcrumb(), url

def prep_cbv(cls, request, kwargs, args):
    instance = cls()
    if hasattr(instance, 'get') and not hasattr(instance, 'head'):
        instance.head = instance.get
    instance.request = request
    instance.args = args
    instance.kwargs = kwargs
    return instance

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

    def set_request_breadcrumbs(self):
        bc_sources = self.request.breadcrumbs.bc_sources
        for cbv, arg_names in bc_sources:
            if not hasattr(cbv, 'breadcrumb'):
                raise ValueError('"%s" invalid breadcrumb view'
                                 % str(cbv))
            # TODO: Fix this:
            arg_count = len(arg_names)
            args = self.args[:arg_count]
            kwargs = {
                key: value for key, value in self.kwargs.items()
                if key in arg_names
            }
            instance = prep_cbv(cbv, self.request, kwargs, args)
            title, url = get_breadcrumb_info_from_view(instance)
            self.request.breadcrumbs.append(title, url)

        # Finally, append current breadcrumb
        title, url = get_breadcrumb_info_from_view(self)
        self.request.breadcrumbs.append(title, url)

    def dispatch(self, *args, **kwargs):
        self.set_request_breadcrumbs()
        return super().dispatch(*args, **kwargs)



