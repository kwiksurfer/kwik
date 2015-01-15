# Create your views here.

from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from people.models import UserProfile

@login_required
def view_profile(request, template_name='profile.html'):
    page_title = 'My Profile'
    user = request.user
    user_profile = user.get_profile()
    friends_list = user_profile.friends.all()
    friends_list2 = user_profile.userprofile_set.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def all_users(request, template_name='users_list.html'):
    page_title = 'All Users'
    user = request.user
    all_users = UserProfile.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def view_user(request, user_id, template_name='profile.html'):
    page_title = 'View User'
    user = get_object_or_404(User, pk=user_id)
    user_profile = user.get_profile()
    friends_list = user_profile.friends.all()
    friends_list2 = user_profile.userprofile_set.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))