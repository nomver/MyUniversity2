from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Profile,MessageToUser
# Register your models here.
class UserAdmin1(UserAdmin):
    list_display=['username','email','is_staff','is_superuser','university','department','you_are','is_hod','is_teacher','is_student']
    list_editable=['university','department','is_student','is_teacher','is_hod']
    list_filter=['university','department','is_student','is_teacher','is_hod','you_are']
admin.site.register(Profile)

admin.site.register(User,UserAdmin1)
admin.site.register(MessageToUser)