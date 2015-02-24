from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.core import urlresolvers
# from django.contrib.contenttypes import generic # for GenericForeignKey

from kwiksurfs.models import Post, NewsCategory #, Picture

# Create your models here.

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='profile')

    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default="M")
    #picture = models.ForeignKey(Picture) # CamelCase, with an uppercase first letter
    friends = models.ManyToManyField("self") # change this. get rid of the through    # DONE!
    newscategories = models.ManyToManyField(NewsCategory)
    joined_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)    # uncomment, then syncdb
    #active = models.BooleanField(default=False) #after a confirmation mail has been sent and confirmation link clicked, user will be activated
    blocked = models.ManyToManyField(User, related_name='blckd+')

    def __unicode__(self):
        return 'User Profile for: ' + self.user.email

    @models.permalink
    def get_absolute_url(self):
        # return urlresolvers.reverse('view_user', kwargs={'user_id': self.user.id})
        return ('view_user_username', (), {'username': self.user.username})

    def full_name(self):
        return self.user.first_name + " " + self.user.last_name

    def unread_messages_count(self):
        conversations = self.user.conversations.filter(messages__seen=False, users__id__exact=self.user.id).distinct()
        return Message.objects.exclude(sender__id=self.user.id).filter(conversation__in=conversations, seen=False).distinct().count()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)

class UserVerifier(models.Model):
    user = models.ForeignKey(User, unique=True)
    passcode = models.IntegerField() # random code included in verification link. When verification is completed, model instance is deleted

class FriendshipRequest(models.Model): # throw away this model and create a friendship request model
    initiator = models.ForeignKey(User, related_name='ini+') #are 'related_name's even necessary?
    acceptor = models.ForeignKey(User, related_name='acc+')
    accepted = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(auto_now=True)

    def get_add_url(self, acceptor_id):
        return urlresolvers.reverse('people.views.add_friend', (), {'acceptor_id': acceptor_id})

    def get_confirm_url(self):
        return urlresolvers.reverse('people.views.confirm_request', (), { 'initiator_id': self.initiator.pk, 'request_id': self.pk, })

    def get_delete_url(self):
        return urlresolvers.reverse('people.views.delete_request', (), { 'initiator_id': self.initiator.pk, 'request_id': self.pk, })

def add_friend_from_request(sender, instance, ** kwargs):    # called when the request is being accepted by the acceptor, just before the request model is deleted
    if instance.accepted:
        the_friend = instance.initiator                          # in this case, the initiator is added to the list of friends of the acceptor
        the_profile = instance.acceptor.get_profile()
        the_profile.friends.add(the_friend)

pre_delete.connect(add_friend_from_request, sender=FriendshipRequest)

class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name="conversations")

    def __unicode__(self):
        return 'Conversation among ' + ", ".join([this_user.get_profile().full_name() for this_user in self.users.all()])

    def get_absolute_url(self):
        #return urlresolvers.reverse('people.views.conversation', (), { 'correspondent_id': self.other_user(user), })       # fix_this!!!
        return urlresolvers.reverse('people.views.conversation_by_id', (), { 'conversation_id': self.id})

    def other_user(self, user):
        for this_user in self.users.all():
            if not this_user == user:
                return this_user

    def unread_messages_count(self, user):
        return self.messages.exclude(sender__id=user.id).filter(seen=False).count()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent', editable=False)
    conversation = models.ForeignKey(Conversation, editable=False, related_name="messages")
    message = models.TextField(default="")
    seen = models.BooleanField(default=False, editable=False)     # I have to add this. For notifying about, and styling new messages
    date_sent = models.DateTimeField(auto_now_add=True, editable=False)   # compulsory!!!

    def __unicode__(self):
        return 'Message from ' + self.sender.username + ' to ' + self.receiver().username

    def receiver(self):
        sender = self.sender
        for user in self.conversation.users.all():
            if not user == sender:
                receiver = user
        return receiver

class UserGroup(models.Model):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=128) # do we really need this? we could just use numbers, couldn't we?
    members = models.ManyToManyField(User, related_name='mem+', through='UserGroupMembership')
    admin = models.ForeignKey(User, related_name='ad+')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Group ' + self.name

class UserGroupMembership(models.Model):
    user = models.ForeignKey(User)
    user_group = models.ForeignKey(UserGroup)
    added = models.BooleanField(default=False) # admin adds and validates requests
    joined_at = models.DateTimeField(auto_now_add=True)

class UserGroupMessage(models.Model):
    sender = models.ForeignKey(User)
    user_group = models.ForeignKey(UserGroup)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'UserGroupMessage from ' + self.sender + ' to UserGroup ' + self.user_group