# Create your views here.

from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from kwiksurfs.models import Post, Comment
from kwiksurfs.forms import PostForm, CommentForm

@login_required
def view_posts(request, user_id=None, template_name='posts.html'):
    # gotta add pagination
    model_name = 'post'
    user = request.user
    user_profile = user.get_profile()
    form = PostForm()
    comment_form = CommentForm()
    friends =  user.get_profile().friends.all()
    if user_id == None:
        posts = Post.objects.filter(Q(privacy='E') | Q(privacy='F', author__profile__in=list(friends)) | Q(author=user))
        #all_posts = Post.objects.filter(privacy='E').filter(privacy='F')#.filter(author=user).filter(privacy='F', author__profile__in=list(friends))
        page_title = "Posts"
    else:
        this_user = get_object_or_404(User, id=user_id)
        # all_posts = Post.objects.filter(author__id=user_id).filter(Q(privacy='E') | Q(privacy='F', author__profile__in=list(friends)))  # let's make this more efficient
        if this_user in friends:
            posts = Post.objects.filter(author__id=user_id).filter(Q(privacy='E') | Q(privacy='F'))     # aha!!!
        else:
            posts = Post.objects.filter(author__id=user_id).filter(Q(privacy='E'))      # now, you're talking!
        page_title = "Posts by " + this_user.username
    # posts = []
    # for this_post in all_posts:
    #     if this_post.can_be_viewed_by(user):
    #         posts.append(this_post)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def new_post(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = PostForm(postdata)
        post = postdata.get("post","")
        if (not unicode.strip(post) == "") and form.is_valid():
            privacy = postdata.get("privacy","")
            new_post = Post(post=post, author=request.user,privacy=privacy)
            new_post.save()
    else:
        form = PostForm()
    return HttpResponseRedirect(urlresolvers.reverse(view_posts))

# possibilities: make a generic 'new_comment' view which will work for all kwiksurfs
#               make a 'new_comment' view which accepts 'model' as a parameter - YES!!!

def new_comment(request, model='post', object_id=None):
    user = request.user
    page_path = request.META.get('HTTP_REFERER', '/')
    content_type = ContentType.objects.get(app_label='kwiksurfs', model=model)
    content_class = content_type.model_class()
    content_object = get_object_or_404(content_class, id=object_id)
    if request.method == 'POST':
        postdata = request.POST.copy()
        comment_form = CommentForm(postdata)
        comment = postdata.get("comment","")
        if (not unicode.strip(comment) == "") and comment_form.is_valid():
            new_comment = Comment(comment=comment, author=user, content_object=content_object)    # change 'content_object' to 'kwiksurf'
            new_comment.save()
    else:
        comment_form = CommentForm()
    return HttpResponseRedirect(page_path)

def get_referrer(request):
    return request.META.get('HTTP_REFERER', '/')
