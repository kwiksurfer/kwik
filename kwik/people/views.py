# Create your views here.

from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate

from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from people.forms import UserChangeForm
from people.forms import UserCreationForm, AuthenticationForm, UserProfileForm, MessageForm, RequestDeleteForm
from people.models import UserProfile, FriendshipRequest, Message, Conversation
from django.db.models import Avg, Sum, Count

def register(request, template_name="register.html"):   # I should remove this view later and add it to the login
    if request.method == 'POST':                        # view. so that both forms may be on the same page.
        postdata = request.POST.copy()                  # okay. maybe not.
        form = UserCreationForm(postdata)               # okay, so I have to have the profile form on this same page.
        if form.is_valid():                             # that's the best thing to do
            form.save()
            us = postdata.get('username','')
            em = postdata.get('email','')
            pw = postdata.get('password1','')
            new_user = authenticate(username=us,password=pw)
            if new_user is not None:
                if new_user.is_active:
                    login(request, new_user)
                    url = urlresolvers.reverse('edit_profile')
                    return HttpResponseRedirect(url)
    else:
        form = UserCreationForm()
        #aform = AuthenticationForm()                   # useful only when I'm using both on the same screen;
    page_title = 'Join kwiksurfer.com'
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


@login_required
def view_profile(request, template_name='profile.html'):
    page_title = 'My Profile'
    user = request.user
    this_user = user
    user_profile = user.get_profile()
    this_user_profile = user_profile
    friends_list = user_profile.friends.all()
    num_messages = (Message.objects.exclude(sender__id__exact=user.id)).filter(conversation__users__id__exact=user.id, seen=False).count()
    # friends_list2 = user_profile.userprofile_set.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def edit_profile(request, template_name="profile-form.html"):
    user = request.user
    profile = user.get_profile()
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserProfileForm(postdata, instance=profile)
        user_form = UserChangeForm(postdata, instance=user)
        if form.is_valid():
            form.save()
            if user_form.is_valid():
                user_form.save()
            url = urlresolvers.reverse('view_profile')
            return HttpResponseRedirect(url)
    else:
        form = UserProfileForm(instance=profile)
        user_form = UserChangeForm(instance=user)
    page_title = 'Edit Profile'
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))

def all_users(request, template_name='users_list.html'):
    page_title = 'All Users'
    user = request.user
    user_profile = user.get_profile()
    profiles = UserProfile.objects.all()   # returns all userprofiles
    users = User.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def view_user(request, user_id=0, username="", template_name='profile.html'):
    page_title = 'View User'
    user = request.user
    if int(user_id) == user.id or username == user.username:
        return HttpResponseRedirect(urlresolvers.reverse('view_profile'))
    user_profile = user.get_profile()
    if not user_id == 0:
        this_user = get_object_or_404(User, pk=user_id)
    else:
        this_user = get_object_or_404(User, username=username)
    this_user_profile = this_user.get_profile()
    friends_list = this_user_profile.friends.all()
    friendship_request = False
    if user_profile in friends_list:     # friendship_request.accepted:
        is_friend = True
        request_sent = 1
    else:
        try:
            friendship_request = FriendshipRequest.objects.get(initiator=user, acceptor=this_user)
            # request_sent = "to"
        except ObjectDoesNotExist:
            try:
                friendship_request = FriendshipRequest.objects.get(initiator=this_user, acceptor=user)
                # request_sent = "from"
            except ObjectDoesNotExist:
                request_sent = 0
        if friendship_request:
            if friendship_request.initiator == user:
                request_sent = "to"
            else:
                request_sent = "from"
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def add_friend(request, acceptor_id):
    the_acceptor = User.objects.get(pk=acceptor_id)
    try:
        FriendshipRequest.objects.get(initiator=request.user,acceptor=the_acceptor)
        exists = True
    except ObjectDoesNotExist:
        exists = False

    if exists:
        message = "You've already sent a request to " + the_acceptor.get_profile().full_name()
        url = urlresolvers.reverse('view_user',kwargs={'user_id':the_acceptor.id})
        return HttpResponseRedirect(url)

    try:
        FriendshipRequest.objects.get(acceptor=request.user,initiator=the_acceptor)
        exists = True
    except ObjectDoesNotExist:
        exists = False

    if exists:
        message = the_acceptor.get_profile().full_name() + " has sent you a request already and is awaiting your confirmation "
        url = urlresolvers.reverse('view_user',kwargs={'user_id':the_acceptor.id})
        return HttpResponseRedirect(url)

    r = FriendshipRequest.objects.create(initiator=request.user, acceptor=the_acceptor)
    r.save()
    message = "You have sent " + the_acceptor.get_profile().full_name() + " a friend request!"
    url = urlresolvers.reverse('view_user',kwargs={'user_id':the_acceptor.id})
    return HttpResponseRedirect(url)

@login_required
def view_requests(request, template_name='requests.html'):
    user = request.user
    page_title = "Friendship Requests"
    requests = FriendshipRequest.objects.filter(acceptor=user, accepted=False).order_by('-sent_at')
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@login_required
def confirm_request(request, request_id, initiator_id, template_name='requests.html'):
    r = get_object_or_404(FriendshipRequest, pk=request_id)
    the_initiator = r.initiator
    the_initiator_profile = the_initiator.get_profile()
    the_acceptor = r.acceptor
    initiator_id = int(initiator_id)
    user = request.user
    user_profile = user.get_profile()
    if not initiator_id == the_initiator.id:
        message = "I think you've made a mistake!"
        url = urlresolvers.reverse('my_profile')
        return HttpResponseRedirect(url)
    if not the_acceptor == user:
        message = "Um... this request is not FOR you!"
        url = urlresolvers.reverse('my_profile')
        return HttpResponseRedirect(url)
    if r.accepted or the_initiator in user_profile.friends.all():
        message = "invalid action"
        url = urlresolvers.reverse('my_profile')
        return HttpResponseRedirect(url)
    r.accepted = True
    r.save()                                    # these three lines could just be replaced by "r.delete()", you know...
    # since I've created the signal listener for post_delete...
    user_profile.friends.add(the_initiator_profile)       # we'll think about which one is better sha.
    message = "You and " + the_initiator_profile.full_name() + " are now friends!"
    url = urlresolvers.reverse('view_user',kwargs={'user_id':the_initiator.id})
    return HttpResponseRedirect(url)

@login_required
def delete_request(request, request_id, initiator_id, template_name='confirm-delete-request.html'):
    r = get_object_or_404(FriendshipRequest, pk=request_id)
    the_initiator = r.initiator
    the_initiator_profile = the_initiator.get_profile()
    the_acceptor = r.acceptor
    initiator_id = int(initiator_id)
    user = request.user
    user_profile = user.get_profile()
    if not initiator_id == the_initiator.id:
        message = "I think you've made a mistake!"
        url = urlresolvers.reverse('my_profile')
        return HttpResponseRedirect(url)
    if not the_acceptor == request.user:
        message = "Um... this request is not FOR you!"
        url = urlresolvers.reverse('my_profile')
        return HttpResponseRedirect(url)
    if r.accepted or the_initiator in user_profile.friends.all():
        message = "invalid action"
        url = urlresolvers.reverse('my_profile')
        return HttpResponseRedirect(url)
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata.get('request_id','') and int(postdata.get('request_id','')) == int(request_id):
            r.delete()
            message = "Request deleted"
        else:
            message = "There was an error"
        url = urlresolvers.reverse('my_profile')
        return HttpResponseRedirect(url)
    else:
        form = RequestDeleteForm({'request_id':request_id})
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def new_message(request, receiver_id=None, template_name='compose-message.html'):
    user = request.user
    receiver = get_object_or_404(User, pk=receiver_id)
    try:
        conversation = Conversation.objects.filter(users__id__exact=user.id).get(users__id__exact=receiver_id)  # retrieve specific convo
    except ObjectDoesNotExist:
        conversation = create_conversation(user, receiver)

    page_title = "New Message"
    if request.method == 'POST':
        postdata = request.POST.copy()
        postdata.update({'conversation_id': conversation.id, 'sender_id': user.id,})     # WATCH!!!
        form = MessageForm(postdata)
        if form.is_valid():
            message = postdata.get('message','')
            conversation_id = conversation.id
            sender_id = user.id
            m = Message(message=message, conversation_id=conversation_id, sender_id=sender_id)
            m.save()
            return HttpResponseRedirect(urlresolvers.reverse('conversation',kwargs={'correspondent_id':receiver_id})) # change this to link to conversation
        else:
            message = "error in message"
            return HttpResponseRedirect(urlresolvers.reverse('new_message'))
    else:
        if not receiver_id == None:
            receiver = User.objects.get(pk=receiver_id)
            form = MessageForm()
        else:
            form = MessageForm()
        return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def conversation(request, correspondent_id=None, template_name='conversation.html'):
    user = request.user

    if correspondent_id == None:
        return HttpResponseRedirect(urlresolvers.reverse('conversations'))
    try:
        correspondent = User.objects.get(pk=correspondent_id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(urlresolvers.reverse('conversations'))
    page_title = "Conversation with " + correspondent.get_profile().full_name()

    try:
        conversation = Conversation.objects.filter(users__id__exact=user.id).get(users__id__exact=correspondent_id)  # retrieve specific convo
    except ObjectDoesNotExist:
        conversation = create_conversation(user, correspondent)

    if request.method == 'POST':
        postdata = request.POST.copy()
        postdata.update({'conversation_id': conversation.id, 'sender_id': user.id,})     # WATCH!!!
        form = MessageForm(postdata)
        if form.is_valid():
            message = postdata.get('message','')
            conversation_id = conversation.id
            sender_id = user.id
            m = Message(message=message, conversation_id=conversation_id, sender_id=sender_id)
            m.save()
            return HttpResponseRedirect(urlresolvers.reverse('conversation',kwargs={'correspondent_id':correspondent_id})) # change this to link to conversation
        else:
            message = "error in message"
            return HttpResponseRedirect(request.path)
    else:
        if not correspondent_id == None:
            receiver = User.objects.get(id=correspondent_id)
            form = MessageForm()
        else:
            form = MessageForm()
    messages = conversation.messages.all().order_by('-date_sent')
    messages.exclude(sender__id__exact=user.id).update(seen=True)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def conversation_by_id(request, conversation_id=None):
    user = request.user
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if not user in conversation.users.all():
        return HttpResponseRedirect(urlresolvers.reverse('conversations'))
    correspondent_id = conversation.other_user(user).id
    return HttpResponseRedirect(urlresolvers.reverse('conversation', kwargs={'correspondent_id': correspondent_id}))

@login_required
def conversations(request, template_name='conversations.html'):
    user = request.user
    conversations = Conversation.objects.filter(users__id__exact=user.id).annotate(message_count=Count('messages'), unread_count=Count('messages'))
    # messages = Message.objects.filter(receiver_id__exact=user.id).filter(sender_id__exact=user.id)#.order_by('-date_sent', 'sender')   # this brings all messages to and from this user and the correspondent
    # distinct_messages = messages.distinct('sender', 'receiver')
    page_title = "Conversations"
    # users = []
    # for conversation in conversations:
    #     for the_user in conversation.users.all():
    #         if not the_user == user:
    #                 users[] = the_user
    latest_messages = Message.objects.filter(conversation__in=conversations).latest('date_sent')
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    conversation = message.conversation
    return HttpResponseRedirect(urlresolvers.reverse('conversation',kwargs={'conversation_id':conversation.id}))

def create_conversation(user1, user2):
    conversation = Conversation.objects.create()       # verify this, please
    conversation.users.add(user1)
    conversation.users.add(user2)
    return conversation