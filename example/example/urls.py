from django.conf.urls import url
from django.contrib import admin
from microblog import views as mb_views

urlpatterns = [
    url(r'^$', mb_views.index),
    url(r'^new-author/$', mb_views.new_author),
    url(r'^new-post/$', mb_views.new_post),
    url(r'^new-follow/$', mb_views.new_follow),

    url(r'^posts/(?P<username>\w{0,50})/$', mb_views.view_posts),
    url(r'^admin/', admin.site.urls),
    # url(r'', include('django_view_hierarchy.urls', namespace='django_view_hierarchy')),
]
