

'''
def view(request, *args, **kwargs):
	self = cls(**initkwargs)
	if hasattr(self, 'get') and not hasattr(self, 'head'):
		self.head = self.get
	self.request = request
	self.args = args
	self.kwargs = kwargs
'''

def prep_cbv_and_get_breadcrumb(cls, request, args, kwargs):
    if cls.breadcrumb:
        return str(cls.breadcrumb)
    self = cls()
    self.request = request
    self.args = args
    self.kwargs = kwargs
    return self.get_breadcrumb()

class BreadcrumbMixin:
    breadcrumb = None

    def get_breadcrumb(self):
        if self.breadcrumb:
            return self.breadcrumb

        if hasattr(self, 'get_object'):
            obj = self.get_object()
            return str(obj)
        return str(self.__name__)  # Default to name of this view

    def set_request_breadcrumbs(self):
        bc_sources = self.request.breadcrumbs.bc_sources
        for bc_source, arg_count in bc_sources:
            if not hasattr(bc_source, 'breadcrumb'):
                raise ValueError('"%s" invalid breadcrumb view'
                                 % str(bc_source))
            args = self.args[:arg_count]
            breadcrumb_str = prep_cbv_and_get_breadcrumb(
                self.request,
                self.kwargs,
                args,
            )
            # self.request.breadcrumbs.append_text(breadcrumb_str)

    def dispatch(self, *args, **kwargs)):
        self.set_request_breadcrumbs()
        super().dispatch(*args, **kwargs)



