from django.shortcuts import render , redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.template.defaultfilters import truncatechars ,safe,escape
from django.db.models import Q


# Create your views here.
def Index(request):
	context = {}
	context['data'] =  BlogPost.objects.filter().order_by('-id').values()[:6]
	for i in context['data']:
		i['short_description'] = truncatechars(strip_tags(i["content"]),250)

		i['comment'] = LeaveComments.objects.filter(post_id=i['id']).count()
		i['rating'] = LeaveComments.objects.filter(post_id=i['id']).aggregate(Sum('star')).get('star__sum')
		if i['rating'] is None:
			i['rating'] = 0
		i['rating'] = int(i['rating'])
		
	return render(request,'index.html',context)

def BlogDetails(request,id):
	context = {}
	if request.POST:
		data = request.POST
		print(data,'data is called ')
		try:
			star = data['star']
		except :
			star = 0

		LeaveComments.objects.create(post_id=id,comment=data['comment'],name=data['name'],star=star,email=data['email'],mobile=data['mobile'])
		return redirect(f'/blog-view/{id}')
	else:
		context['blog'] =  BlogPost.objects.get(id=id)
		context['image'] = Image.objects.filter(post_id=id)
		context['video'] = Video.objects.filter(post_id=id)

	return render(request,'view_blog.html',context)

from django.contrib.humanize.templatetags.humanize import naturaltime


def AllBlog(request):
	return render(request,'blog_collection.html')

@csrf_exempt
def BlogPOSTAPI(request,id):

	context= {}
	data = request.POST
	print("data is called ")
	print(data)
	if data['rating'] is None:
		data['rating'] = 0

	check  = BlogPost.objects.filter(id=id)
	if check.exists():
		LeaveComments.objects.create(post_id=id,comment=data['comment'],star=data['rating'],email=data['email'],mobile=data['mobile'])
		context['status_flag'] = True
	else:
		context['status_flag'] = False
	return JsonResponse(context)


def BlogData(request,id):
	context = {}
	context['data'] = list(LeaveComments.objects.filter(post_id=id).order_by('-id').values())
	for i in context['data']:
		i['ago_date'] = naturaltime(i['created_at'])
	print(context)
	return JsonResponse(context)


@csrf_exempt
def GetInTouchView(request):
	data = json.loads(request.body)
	print(data)

	context={}
	context['email'] = data['email']
	context['mobile'] = data['phone']
	context['name']=data['name']
	context['message'] = data['message']

	GetInTouch.objects.create(**context)
	context['status_flag'] = True
	return JsonResponse(context)


@csrf_exempt
def LeaveCommentPost(request,id):
	data = json.loads(request.body)
	user = request.user
	context = {}
	blog = BlogPost.objects.filter(id=id)
	if blog.exists():
		context['status_flag'] = True
		LeaveComments.objects.create(post_id=id,comment=data['message'],star=data['star'],name = data['name'],email = data['email'],mobile=data['mobile'])
	else:
		context['status_flag'] = False

	print(data)
	return JsonResponse(context)

def LeaveCommentGet(request,id):
	user = request.user
	context = {}
	blog = LeaveComments.objects.filter(post_id=id).order_by('-id').values('id','comment','created_at','star','name','email','mobile')
	print(blog)
	for i in blog:
		i['created_at'] = naturaltime(i['created_at'])
		# replay_data = CommentReply.objects.filter(comment_id=i['id']).order_by('-id').values('id','user__full_name','user__image','reply','created_at')
		# for j in replay_data:
		# 	j['created_at'] = naturaltime(j['created_at'])
		# i['replay_data'] =list(replay_data)
	context['data'] = list(blog)
	context['count'] = blog.count()
	return JsonResponse(context)

from django.db.models import Sum
from django.utils.html import strip_tags


def AllBlogAPI(request):
	context = {}
	search = request.GET['search']
	if search is not None or searh != "":
		search = search.replace('%20'," ")
		s = Q(title__icontains=search)
	else:
		s = Q()
	
	blog = BlogPost.objects.filter().filter(s).values('id','title','content','update_at','create_at','banner_image')
	for i in blog:
		i['comment'] = LeaveComments.objects.filter(post_id=i['id']).count()
		i['rating'] = LeaveComments.objects.filter(post_id=i['id']).aggregate(Sum('star')).get('star__sum')
		if i['rating'] is None:
			i['rating'] = 0
		i['rating'] = int(i['rating'])
		i['short_description'] = truncatechars(strip_tags(i["content"]),250)
		i['create_at'] = naturaltime(i['create_at'])

	context['blog'] = list(blog)
	print(context)
	return JsonResponse(context)
