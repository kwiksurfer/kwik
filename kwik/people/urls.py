from django.conf.urls import patterns, include, url



users_patterns = patterns('people.views',
    # Examples:
    (r'^all/$', 'all_users', {'template_name': 'users_list.html'}, 'all_users'),   # just a test. EXCELLENT!
    (r'^(?P<user_id>[-\d]+)/$', 'view_user', {'template_name': 'profile.html'}, 'view_user'),
    (r'^(?P<username>[-\w]+)/$', 'view_user', {'template_name': 'profile.html'}, 'view_user_username'),
    # url(r'^(?P<user_id>[-\d]+)/block/$', 'block_user'),
)

friends_patterns = patterns('people.views',
    url(r'^add/(?P<acceptor_id>[-\d]+)/$', 'add_friend', {}, 'add_friend'),
    url(r'^confirm_request/(?P<request_id>[-\d]+)/(?P<initiator_id>[-\d]+)/$', 'confirm_request', {}, 'confirm_request'),
    url(r'^delete_request/(?P<request_id>[-\d]+)/(?P<initiator_id>[-\d]+)/$', 'delete_request', {}, 'delete_request'),
    url(r'^view_requests/$', 'view_requests', {'template_name': 'requests.html'}, 'view_requests'),
)

accounts_patterns = patterns('people.views',
    (r'^register/$', 'register', {}, 'register'),
)

accounts_patterns += patterns('django.contrib.auth.views',
    (r'^login/$', 'login', {'template_name': 'login.html'}, 'login'),
    # (r'^accounts/register/$', 'register'),
    (r'^logout/$', 'logout', {}, 'logout'),
)

profile_patterns = patterns('people.views',
    url(r'^$', 'view_profile', {'template_name': 'profile.html'}, 'view_profile'),
    url(r'^$', 'view_profile', {'template_name': 'profile.html'}, 'my_profile'),
    url(r'^edit/$', 'edit_profile', {'template_name': 'profile-form.html'}, 'edit_profile'),
)

messages_patterns = patterns('people.views',
    # url(r'^messages/$', 'all_messages'),
    # url(r'^messages/(?P<correspondent_id>[-\d]+)/$', 'user_messages'),
    url(r'^new/(?P<receiver_id>[-\d]+)/$', 'new_message', {'template_name': 'compose-message.html'}, 'new_message'),
    url(r'^new/$', 'new_message', {}, 'new_message'),

    url(r'^conversation/(?P<correspondent_id>[-\d]+)/$', 'conversation', {'template_name': 'conversation.html'}, 'conversation'),
    url(r'^conversation_by_id/(?P<conversation_id>[-\d]+)/$', 'conversation_by_id', {}, 'conversation_by_id'),
    url(r'^conversations/$', 'conversations', {'template_name': 'conversations.html'}, 'conversations'),
)

# groups_patterns = patterns('people.views',
#     # url(r'^$', 'user_groups'),    # groups the user belongs to (pagination oooo!)
#     # url(r'^all/$', 'all_groups'), # all groups    (pagination oooo!) Generic views and ListView, youknow - no jare
#     # url(r'^create/$', 'create_group'),
#     # url(r'^(?P<group_id>[-\d]+)/$', 'view_group'),    # Generic views and DetailView - no jare
#     # url(r'^(?P<group_id>[-\d]+)/join/$', 'join_group'),
#     # url(r'^(?P<group_id>[-\d]+)/leave/$', 'leave_group'),
#     # url(r'^(?P<group_id>[-\d]+)/messages/$', 'group_messages'),
#     # url(r'^(?P<group_id>[-\d]+)/messages/new/$', 'new_group_message'),
# )

urlpatterns = patterns('people.views',
    # Examples:

    (r'^users/', include(users_patterns)),
    (r'^friends/', include(friends_patterns)),
    (r'^accounts/', include(accounts_patterns)),
    (r'^profile/', include(profile_patterns)),
    (r'^messages/', include(messages_patterns)),
    # (r'^groups/', include(groups_patterns)),      # activate for groups
    # url(r'^verify_user/(?P<user_id>[-\d]+)/(?P<passcode>[-\w]+)$', 'verify_user'),

    # url(r'^kwik/', include('kwik.foo.urls')),
)