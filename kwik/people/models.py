from django.db import models
from django.contrib.auth.models import User
#from django.contrib.contenttypes import generic # for GenericForeignKey

from kwiksurfs.models import Post #, NewsCategory, Picture

# Create your models here.

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

blankPost = Post(post='')

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    #picture = models.ForeignKey(Picture) # CamelCase, with an uppercase first letter
    status = models.ForeignKey(Post, default=blankPost)
    friends = models.ManyToManyField("self", through='Friendship', symmetrical=False) # change this. Use a relationship model and have from (initiator) and to (acceptor)
    #newscategories = models.ManyToManyField(NewsCategories)
    joined_at = models.DateTimeField(auto_now_add=True)
    #active = models.BooleanField(default=False) #after a confirmation mail has been sent and confirmation link clicked, user will be activated

    def __unicode__(self):
        return 'User Profile for: ' + self.user.email

    @models.permalink
    def get_absolute_url(self):
        return ('people.views.view_user', (), { 'user_id': self.pk })

    #def get_absolute_url(self): #after making views

class UserVerifier(models.Model):
    user = models.ForeignKey(User, unique=True)
    passcode = models.IntegerField() # random code included in verification link. When verification is completed, model instance is deleted

class Friendship(models.Model):
    initiator = models.ForeignKey(UserProfile, related_name='ini+') #are 'related_name's even necessary?
    acceptor = models.ForeignKey(UserProfile, related_name='acc+')
    accepted = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sen+')
    receiver = models.ForeignKey(User, related_name='rec+')

    def __unicode__(self):
        return 'Message from ' + self.sender.username + ' to ' + self.receiver.username

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

class Block(models.Model):
    blocker = models.ForeignKey(User, related_name='blo+')
    target = models.ForeignKey(User, related_name='tar+')
    blocked_at = models.DateTimeField(auto_now_add=True)