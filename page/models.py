from django.db import models

# Create your models here.
from djrichtextfield.models import RichTextField
from django.template.defaultfilters import truncatechars ,safe,escape
from django.utils.html import strip_tags


class BlogPost(models.Model):
	title = models.CharField(max_length=1000,blank=True,null=True)
	content = RichTextField()
	banner_image = models.ImageField(upload_to ='Post/',blank=True,default='not-available.png')
	update_at = models.DateTimeField(auto_now=True)
	create_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	@property
	def short_description(self):
		return strip_tags(self.content)

		
class Image(models.Model):
	def image_path(instance,filename): 
	# file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
		return f'{instance.post.title}/{filename}'

	post = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
	image = models.ImageField(upload_to=image_path)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Video(models.Model):

	post = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
	video = models.TextField(blank=True,default="")
	# video = models.URLField(max_length=1000, blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class LeaveComments(models.Model):
	post = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
	comment = models.TextField(blank=True,null=True)
	star = models.FloatField(default=0)
	name =models.CharField(max_length=200,null=True,blank=True)
	email = models.EmailField(blank=True,null=True)
	mobile = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class GetInTouch(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=200,null=True,blank=True)
    mobile = models.CharField(max_length=200,null=True,blank=True)
    message = models.CharField(max_length=200,null=1000,blank=True)
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
