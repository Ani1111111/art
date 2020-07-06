from django.contrib import admin
from articles.models import FollowUser, MyPost, PostComment, PostLike,MyProfile,Contact
from django.contrib.admin.options import ModelAdmin

# Register your models here.
class FollowUserAdmin(ModelAdmin):
    list_display = ['followed_by','profile']
    search_fields = ['followed_by','profile']
    list_filter = ['followed_by','profile']
admin.site.register(FollowUser, FollowUserAdmin)

class ContactAdmin(ModelAdmin):
    list_display = ['name','email','msg']
    search_fields = ['name','email','msg']
    list_filter = ['name','email','msg']
admin.site.register(Contact, ContactAdmin)

class MyPostAdmin(ModelAdmin):
    list_display = ['title','cr_date','author','flag']
    search_fields =  ['title','cr_date','author','content','flag']
    list_filter = ['cr_date','author','flag']
admin.site.register(MyPost, MyPostAdmin)

class MyProfileAdmin(ModelAdmin):
    list_display = ['name']
    search_fields =  ['name','status','phone_no']
    list_filter = ['name','phone_no']
admin.site.register(MyProfile, MyProfileAdmin)


class PostCommentAdmin(ModelAdmin):
    list_display = ['post','msg','flag']
    search_fields =  ['msg','post','commented_by','flag']
    list_filter = ['cr_date','flag']
admin.site.register(PostComment, PostCommentAdmin)

class PostLikeAdmin(ModelAdmin):
    list_display = ['post','value','cr_date']
    search_fields =  ['post','value','cr_date']
    list_filter = ['cr_date']
admin.site.register(PostLike, PostLikeAdmin)