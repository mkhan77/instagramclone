from django import forms
from .models import Account, Picture, Comment


class SignUpForm(forms.ModelForm):
	password = forms.CharField(max_length = 100, widget=forms.PasswordInput())
	class Meta:
		model = Account
		fields = ['email', 'full_name', 'user_name', 'password']

class LoginForm(forms.Form):
	user_name = forms.CharField(max_length = 100)
	password = forms.CharField(max_length = 100, widget=forms.PasswordInput())

class EditProfileForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ['profile_pic', 'bio', 'password']

class PictureForm(forms.ModelForm):
	class Meta:
		model = Picture
		fields = ['image', 'caption']

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']

class SearchBar(forms.Form):
	search = forms.CharField(max_length = 254)

class PasswordReset(forms.ModelForm):
	class Meta:
		model = Account
		fields = ['email']
	


	