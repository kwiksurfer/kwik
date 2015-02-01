from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('people.views',
    # Examples:

    url(r'^profile/$', 'view_profile', {}, 'view_profile'),
    url(r'^profile/$', 'view_profile', {}, 'my_profile'),
    (r'^view_user/(?P<user_id>[-\w]+)/$', 'view_user', {}, 'view_user'),
    (r'^users/(?P<username>[-\w]+)/$', 'view_user', {}, 'view_user_username'),
    (r'^all_users/$', 'all_users', {'template_name': 'users_list.html'}, 'all_users'),   # just a test
    (r'^accounts/register/$', 'register', {}, 'register'),
    (r'^edit_profile/$', 'edit_profile', {}, 'edit_profile'),
    url(r'^add_friend/(?P<acceptor_id>[-\w]+)/$', 'add_friend', {}, 'add_friend'),
    url(r'^confirm_request/(?P<request_id>[-\w]+)/(?P<initiator_id>[-\w]+)/$', 'confirm_request', {}, 'confirm_request'),
    url(r'^delete_request/(?P<request_id>[-\w]+)/(?P<initiator_id>[-\w]+)/$', 'delete_request', {}, 'delete_request'),
    url(r'^view_requests/$', 'view_requests', {}, 'view_requests'),

    # url(r'^verify_user/(?P<user_id>[-\w]+)/(?P<passcode>[-\w]+)$', 'verify_user'),
    # url(r'^messages/$', 'all_messages'),
    # url(r'^messages/(?P<correspondent_id>[-\w]+)/$', 'user_messages'),
    url(r'^new_message/(?P<receiver_id>[-\w]+)/$', 'new_message', {}, 'new_message'),
    url(r'^new_message/$', 'new_message', {}, 'new_message'),

    url(r'^conversation/(?P<correspondent_id>[-\w]+)/$', 'conversation', {}, 'conversation'),
    url(r'^conversations/$', 'conversations', {}, 'conversations'),
    # url(r'^groups/$', 'user_groups'),
    # url(r'^all_groups/$', 'all_groups'), # for starters
    # url(r'^create_group/$', 'create_group'),
    # url(r'^group/(?P<group_id>[-\w]+)/$', 'view_group'),
    # url(r'^join_group/(?P<group_id>[-\w]+)/$', 'join_group'),
    # url(r'^leave_group/(?P<group_id>[-\w]+)/$', 'leave_group'),
    # url(r'^group_messages/(?P<group_id>[-\w]+)/$', 'group_messages'),
    # url(r'^new_group_message/(?P<group_id>[-\w]+)/$', 'new_group_message'),
    # url(r'^block_user/(?P<user_id>[-\w]+)/$', 'block_user'),
    # url(r'^kwik/', include('kwik.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)

urlpatterns += patterns('django.contrib.auth.views',
    (r'^accounts/login/$', 'login', {'template_name': 'login.html'}),
    # (r'^accounts/register/$', 'register'),
    (r'^accounts/logout/$', 'logout'),
)