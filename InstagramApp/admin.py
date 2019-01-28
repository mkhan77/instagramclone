from django.contrib import admin
from .models import Account, Picture, Comment

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
	list_display = ['full_name', 'user_name', 'email']
	class Meta:
		model = Account


class PictureAdmin(admin.ModelAdmin):
	list_display = ['id', 'date_uploaded']
	class Meta:
		model = Picture

class CommentAdmin(admin.ModelAdmin):
	list_display = ['id', 'user']
	class Meta:
		model = Comment

admin.site.register(Account, AccountAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Comment, CommentAdmin)