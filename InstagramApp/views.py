from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import (
	SignUpForm, 
	LoginForm, 
	EditProfileForm, 
	PictureForm, 
	CommentForm,
	SearchBar,
)
from .models import Account, Picture, Comment
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.


def signup(request):
	form = SignUpForm(request.POST or None)
	message = ''
	if request.method == 'POST':
		if form.is_valid():
			instance = form.save(commit = False)
			message = "Success! The new Account has been created."
			instance.save()
			form = SignUpForm(None)
		
	context = {
		'form': form,
		'message': message,
	}
	return render(request, 'base.html', context)

def getUserID():
	f = open('InstagramApp/loggeduserid.txt', 'r')
	logged_userid = int(f.read())
	f.close()
	return logged_userid


def login(request):
	try:
		form = LoginForm(request.POST or None)
		if form.is_valid():
			user_name = form.cleaned_data.get('user_name')
			password = form.cleaned_data.get('password')
			act = Account.objects.get(user_name = user_name, password = password)
			f = open('InstagramApp/loggeduserid.txt', 'r+')
			f.write(str(act.id))
			f.close()
			act.save()
			return profilePage(request, act.id)
		else:
			context = {'form': form}
			return render(request, 'login.html', context)
	except Account.DoesNotExist:
		message = 'Sorry the Username or the Password was entered incorrectly. Try again.'
		context = {
			'form': form,
			'message': message,
		}
		return render(request, 'login.html', context)


def profilePage(request, id):
	act = Account.objects.get(id = id)
	logged_userid = getUserID()
	user_act = Account.objects.get(id = logged_userid)
	act.followers_num = len(list(act.followed_by.all()))
	act.following_num = len(act.following.all()) #the len function can actually be called on the query set without converting to list
	act.posts_num = len(act.picture_library.all())
	act.save()
	return render(request, 'profile_page.html', {'account': act, 'user_id': logged_userid, 'user_act':user_act})


def follow(request, followedUser_id):
	logged_userid = getUserID()
	act = Account.objects.get(id = logged_userid)
	actFollowed = Account.objects.get(id = followedUser_id)
	act.following.add(actFollowed)
	# act.save()
	# actFollowed.save()
	return profilePage(request, actFollowed.id)


def editProfile(request, id):
	act = Account.objects.get(id = id)
	form = EditProfileForm(request.POST or None, request.FILES or None, instance = act)
	message = ''
	logged_userid = getUserID()
	if request.method == 'POST':
		if form.is_valid():
			instance = form.save(commit = False)
			instance.save()
			message = "Changes Saved."
			form = EditProfileForm(request.POST, request.FILES)
			return HttpResponseRedirect('/profilepage/%d' %logged_userid)
	context = {
		'form': form,
		'message': message,
		'account': act,
		# 'user_id': logged_userid
	}
	return render(request, 'editprofile.html', context)


def showAllProfiles(request):
	logged_userid = getUserID()
	act = Account.objects.get(id=logged_userid)
	profiles = Account.objects.all()
	form = SearchBar(request.GET or None)
	context = {
		"account": profiles, 
		'user': act, 
		'form': form
		}
	#searching for profiles
	
	if request.method == 'GET':
		if form.is_valid():
			user_search = form.cleaned_data.get('search')
			results = Account.objects.filter(user_name__icontains = user_search)
			form = SearchBar(request.GET)
			context = {
				"account": results,
				"form": form, 
				'user': act
			}
	
	return render(request, 'allprofiles.html', context)


def uploadPicture(request):
	logged_userid = getUserID()
	user_act = Account.objects.get(id = logged_userid)
	form = PictureForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			instance = form.save(commit = False)
			instance.user = user_act
			instance.save()
			user_act.posts_num += 1
			user_act.picture_library.add(instance)
			form = PictureForm(request.POST, request.FILES)	
			user_act.save()
			return HttpResponseRedirect('/profilepage/%d' %logged_userid)
	context = {
		'form': form,
		'account': user_act,
		'user_id': logged_userid
	}
	return render(request, 'upload_picture.html', context)


def showPicture(request, id, username):
	logged_userid = getUserID()
	act = Account.objects.get(user_name=username)
	pic = Picture.objects.get(id=id)
	comment_by = Account.objects.get(id = logged_userid)
	pic.likes = len(pic.like_users.all())
	form = CommentForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			instance = form.save(commit = False)
			content = form.cleaned_data.get('content')
			new_comment = Comment.objects.create(content = content, user = comment_by, on_picture = pic)
			pic.comments.add(new_comment)
			form = CommentForm(request.POST)
			return HttpResponseRedirect('/showpicture/%d/%s' %(pic.id, act.user_name))
	context = {
		'picture': pic,
		'account': act,
		'user': comment_by,
		'form': form,
	}
	return render(request, 'picture.html', context)


def like(request, pic_id):
	pic = Picture.objects.get(id=pic_id)
	logged_userid = getUserID()
	user_act = Account.objects.get(id = logged_userid)
	pic.like_users.add(user_act)
	pic.likes = len(pic.like_users.all())
	pic.save()
	context = {
		'picture': pic,
		'account': pic.user,
	}
	return showPicture(request, pic_id, pic.user.user_name)
	# return render(request, 'picture.html', context)

def unlike(request, pic_id):
	pic = Picture.objects.get(id=pic_id)
	logged_userid = getUserID()
	user_act = Account.objects.get(id = logged_userid)
	pic.like_users.remove(user_act)
	pic.likes = len(pic.like_users.all())
	pic.save()
	context = {
		'picture': pic,
		'account': pic.user,
	}
	return HttpResponseRedirect('/showpicture/%d/%s' %(pic.id, pic.user))
	# context = {
	# 	'picture': pic,
	# 	'account': act,
	# }
	# return render(request, 'picture.html', context)


def unfollow(request, unfollowedUser_id):
	logged_userid = getUserID()
	user_act = Account.objects.get(id = logged_userid)
	actunFollowed = Account.objects.get(id = unfollowedUser_id)
	user_act.following.remove(actunFollowed)
	user_act.save()
	actunFollowed.save()
	return profilePage(request, actunFollowed.id)


def search(request):
	form = SearchBar(request.GET or None)
	results = Account.objects.all()
	if request.method == 'GET':
		if form.is_valid():
			instance = form.save(commit = False)
			user_search = form.cleaned_data.get('search')
			results = Account.objects.filter(user_name = user_search)
			form = SearchBar(request.GET)
			context = {
				"account": results,
				"form": form
			}
			return render(request, 'allprofiles.html', context)


def deleteAccount(request):
	act = Account.objects.get(user_name)
	act.delete()
	return HttpResponse('Account Deleted')



