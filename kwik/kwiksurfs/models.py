from django.core import urlresolvers
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic # for GenericForeignKey. chill for now
from django.contrib.contenttypes.models import ContentType
# Create your models here.

PRIVACY_CHOICES = (
    ('E', 'Everyone'),
    ('F', 'Friends'),
    ('M', 'Me alone'),
)

class Post(models.Model):
    post = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES)
    #rating = models.ForeignKey('Rating', default=default_rating)
    comments = generic.GenericRelation('Comment')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-added_at']

    def __unicode__(self):
        return 'Post: ' + self.post

    def can_be_viewed_by(self, user):
        if self.author == user or (self.privacy == 'F' and user.get_profile() in self.author.get_profile().friends.all()) or self.privacy == 'E':
            return True
        return False

    def comment_submit_url(self):
        urlresolvers.reverse('new_comment', {'model':'post', 'object_id':self.id,})
        pass


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')     # change this to kwiksurf
    is_deleted = models.BooleanField(default=False)
    # added_at = models.DateTimeField(auto_now_add=True)    # why did I forget this guy? ehn?

    class Meta:
        # ordering = ['added_at']
        pass

    def __unicode__(self):
        return self.author.username + " said: " + self.comment

class Rating(models.Model):
    users = models.ManyToManyField(User)     # quantity is size of this field? if user is here, they cannot rate object again
    value = models.DecimalField(max_digits=4, decimal_places=2)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return 'A rating of ' + self.value + ' from ' + self.quantity() + ' samples'

    def quantity(self):
        return self.users.count()

    def rate(self, _user, _value):
        if _user in self.users.all():
            return "You have rated this kwiksurf already"
        cur_quantity = self.quantity()
        total = self.value * cur_quantity
        total += _value
        self.users.add(_user)
        self.value = total / (cur_quantity + 1)
        self.save()
        return "You have successfully rated this kwiksurf"


class NewsCategory(models.Model):
    name = models.CharField(max_length="20")
    description = models.CharField(max_length="200")

    def __unicode__(self):
        return 'News under category ' + self.name

class News(models.Model):
    title = models.CharField(max_length="50")
    news = models.TextField()
    url = models.URLField()
    category = models.ManyToManyField(NewsCategory)
    comments = generic.GenericRelation(Comment)
    is_deleted = models.BooleanField(default=False)

# class Share / KwikShare