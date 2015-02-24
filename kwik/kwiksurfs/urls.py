from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# from kwiksurfs.views import new_comment

urlpatterns = patterns('kwiksurfs.views',
    # Examples:

    #url(r'^post/(?P<post_id>[-\w]+)/$', 'view_post'),
    # url(r'^(P<object_id>[-\w]+)/$', 'new_comment', {'model':'post'}, name="add_new_comment"),    # add a comment to a post. commenting on other kwiksurfs will have the same form url form
    url(r'^posts/new/$', 'new_post', {}, 'new_post'),
    url(r'^posts/all/$', 'view_posts', {}, 'view_posts'),
    url(r'^posts/(?P<user_id>[-\w]+)/$', 'view_posts', {}, 'view_posts'),    # view user posts
    url(r'^posts/post/(?P<object_id>[-\w]+)/comments/new/$', 'new_comment', {'model':'post'}, name="add_new_comment"),    # add a comment to a post. commenting on other kwiksurfs will have the same form url form
    # url(r'^posts/post/(P<post_id>[-\w]+)/$', 'view_post', {}, 'view_post'),
    # url(r'^kwiksurfs/all/$', 'view_kwiksurfs', {}, 'view_kwiksurfs'),       # view kwiksurfs. This will soon be the main page
    # url(r'^kwiksurfs/(P<user_id>[-\w]+)/$', 'view_kwiksurfs', {}, 'view_kwiksurfs'),    # view user kwiksurfs.

    # url(r'^kwik/', include('kwik.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
