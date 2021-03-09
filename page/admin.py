
from django.contrib import admin
from .models import *
# Register your models here.


class ImageAdmin(admin.TabularInline):
	model = Image
	extra = 1



class VideoAdmin(admin.TabularInline):
	model = Video
	extra = 1



class BlogPostdmin(admin.ModelAdmin):
	list_display = ['title','short_description','update_at','create_at']
	search_fields = ['title','content']
	inlines = [ImageAdmin,VideoAdmin]

admin.site.register(BlogPost,BlogPostdmin)

class LeaveCommentsAdmin(admin.ModelAdmin):
	list_display = ['post','star','comment','name','email','mobile']

admin.site.register(LeaveComments,LeaveCommentsAdmin)



class GetInTouchAdmin(admin.ModelAdmin):
    list_display = ['name','email','mobile','message','create_at','update_at']
