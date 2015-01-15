from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PRIVACY_CHOICES = (
    ('E', 'Everyone'),
    ('F', 'Friends'),
)

class Post(models.Model):
    post = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES)
    #rating = models.ForeignKey(Rating, default=default_rating)

    def __unicode__(self):
        return 'Post: ' + self.post


class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return 'Comment by ' + self.user.username + ' on '

class Rating(models.Model):
    quantity = models.BigIntegerField()
    value = models.DecimalField(max_digits=4, decimal_places=2)

    def __unicode__(self):
        return 'A rating of ' + self.value + ' from ' + self.quantity + 'samples'