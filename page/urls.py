
from django.contrib import admin
from django.urls import path,re_path,include
from .views import *
urlpatterns = [
  path('',Index,name='index'),
  re_path(r'blog-view/(?P<id>\d+)/',BlogDetails,name='blog-view'),
  re_path(r'blog-post-api/(?P<id>\d+)/',BlogPOSTAPI,name='blog-post-api'),

  re_path(r'blog-data/(?P<id>\d+)/',BlogData,name='blog-data'),
     path('get-in-touch/',GetInTouchView,name='get-in-touch'),

         path('all-blog/',AllBlog,name='all-blog'),


   re_path(r'^leave-comment-post/(?P<id>\d+)/$',LeaveCommentPost,name='leave-comment-post'),

   re_path(r'^leave-comment/(?P<id>\d+)/$',LeaveCommentGet,name='leave-comment'),

      re_path(r'^all-blog-api/$',AllBlogAPI,name='all-blog-api'),



   ]
