from __future__ import unicode_literals

from django.db import models
from django import forms

# Create your models here.

class Account(models.Model):
	full_name = models.CharField(max_length = 200)
	email = models.EmailField(max_length = 254, unique = True)
	user_name = models.CharField(max_length = 100, unique = True)
	password = models.CharField(max_length = 100)
	profile_pic = models.ImageField(blank = True)
	bio = models.TextField(max_length = 150, blank = True)
	#this attribute is not needed because of the related name attribute followed_by
	# followers = models.ManyToManyField('self',  blank = True) 
	following = models.ManyToManyField('self', blank = True, symmetrical = False, related_name= 'followed_by')
	picture_library = models.ManyToManyField('Picture', blank = True)
	posts_num = models.PositiveIntegerField(default = 0)
	followers_num = models.PositiveIntegerField(default = 0)
	following_num = models.PositiveIntegerField(default = 0)
	
	def __str__(self):
		return self.user_name
	
	def get_absolute_url(self):
		return "/account/%i/" % self.id


class Picture(models.Model):
	image = models.ImageField()
	caption = models.TextField()
	user = models.ForeignKey('Account', on_delete = models.CASCADE, related_name = 'by_user')
	likes = models.PositiveIntegerField(default = 0)
	like_users = models.ManyToManyField('Account')
	comments = models.ManyToManyField('Comment', blank = True)
	comments_num = models.PositiveIntegerField(default = 0)
	# private = models.BooleanField(blank=True)
	date_uploaded = models.DateTimeField(auto_now = False, auto_now_add = True)

	def __str__(self):
		return str(self.id)

# need to fix the relations i have from account to picture to comments, using foreignkey is better than M2M field in some cases.
	

class Comment(models.Model):
	content = models.TextField(max_length = 250)
	user = models.ForeignKey('Account', on_delete = models.CASCADE)
	on_picture = models.ForeignKey('Picture', on_delete = models.CASCADE)

	def __str__(self):
		return str(self.user)