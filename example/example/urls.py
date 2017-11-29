from django.conf.urls import url
from microblog import views
from django_view_hierarchy.helpers import view_hierarchy

urlpatterns = view_hierarchy({
    '': views.home,
    'about': {
        '': views.about,
        'contact': views.about_contact,
    },
    'posts': {
        '': views.all_authors,
        '(?P<username>\w{0,50})/': views.view_posts,
    },
}) + [
    url(r'^creation/$', views.creation),

    url(r'^new-author/$', views.new_author),
    url(r'^new-post/$', views.new_post),
    url(r'^new-follow/$', views.new_follow),

    #url(r'^admin/', admin.site.urls),
    # url(r'', include('django_view_hierarchy.urls', namespace='django_view_hierarchy')),
]
