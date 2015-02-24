
from people.models import UserProfile, UserGroup, UserGroupMessage, Message, FriendshipRequest, Conversation
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(UserGroup)
admin.site.register(UserGroupMessage)
admin.site.register(Message)
admin.site.register(FriendshipRequest)

class MessageInline(admin.StackedInline):
    model = Message
    #can_delete = False
    verbose_name_plural = 'messages'
    actions = ['mark_seen']

def mark_seen(modeladmin, request, queryset):
    queryset.update(read=True)

class ConversationAdmin(admin.ModelAdmin):
    inlines = (MessageInline, )

admin.site.register(Conversation, ConversationAdmin)