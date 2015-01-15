
from people.models import UserProfile, UserGroup, UserGroupMessage, Block, Message, Friendship
from django.contrib import admin
from django.contrib.auth.models import User
'''
class UserInline(admin.StackedInline):
    model = User
    extra = 3
'''
admin.site.register(UserProfile)
admin.site.register(UserGroup)
admin.site.register(UserGroupMessage)
admin.site.register(Message)
admin.site.register(Block)
admin.site.register(Friendship)