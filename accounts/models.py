from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from uni_app.models import Program,University,Department
CHOICES=[('Student','Student'),('Teacher','Teacher')]
class User(AbstractUser):
    you_are=models.CharField(choices=CHOICES,max_length=100)
    is_student=models.BooleanField(blank=True,default=True)
    is_teacher=models.BooleanField(blank=True,default=False)
    is_hod=models.BooleanField(default=False)
    department=models.ForeignKey(Department,related_name='dept_users',on_delete=models.CASCADE,blank=True,null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='user_profile', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='media/profile/images/', blank=True)
    program=models.ForeignKey(Program,related_name='program_users',on_delete=models.PROTECT,null=True,blank=True)
    Rollnumber=models.PositiveIntegerField(null=True,blank=True)
    CNIC_number=models.PositiveIntegerField(help_text='Without Dashes',blank=True,null=True)

    def __str__(self):
        return str(self.user.username)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.user_profile.save()

# def post_save_profile(sender, instance, created, *args, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# post_save.connect(post_save_profile, sender=settings.AUTH_USER_MODEL)

class MessageToUser(models.Model):
    message=models.TextField()
    from_teacher=models.ForeignKey(User,related_name='teacher_msg',on_delete=models.CASCADE)
    to_student=models.ForeignKey(User,related_name='student_msg',on_delete=models.CASCADE)
    sent_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message

