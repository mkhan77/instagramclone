from django.conf.urls import url
from . import views
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from .forms import PasswordReset
from django.contrib.auth.forms import PasswordChangeForm

urlpatterns = [
	url(r'^$', views.signup, name = 'signup'),
	url(r'^login/$', views.login, name = 'login'),
	url(r'^profilepage/(?P<id>[\d]+)/$', views.profilePage, name = 'profilepage'),
	url(r'^editprofile/(?P<id>[\d]+)/$', views.editProfile, name = 'editprofile'),
	url(r'^allprofiles/$', views.showAllProfiles, name = 'allprofiles'),
	url(r'^uploadpicture/$', views.uploadPicture, name = 'uploadpicture'),
	url(r'^showpicture/(?P<id>[\d]+)/(?P<username>[\w]+)/$', views.showPicture, name = 'showpicture'),
	url(r'^follow/(?P<followedUser_id>[\w]+)/$', views.follow, name = 'follow'),
	url(r'^unfollow/(?P<unfollowedUser_id>[\w]+)/$', views.unfollow, name = 'unfollow'),
	url(r'^likepicture/(?P<pic_id>[\d]+)/$', views.like, name = 'like'),
	url(r'^unlikepicture/(?P<pic_id>[\d]+)/$', views.unlike, name = 'unlike'),
	url(r'^search/$', views.search, name = 'search'),
	#reseting password
	url(r'^reset-password$', password_reset, {'password_reset_form': PasswordReset }, name = 'password-reset'),
	url(r'^reset-password/done$', password_reset_done, name = 'password_reset_done'),
	url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name = 'password_reset_confirm'),
	url(r'^reset-password/complete$', password_reset_complete, name = 'password_reset_complete'),
]