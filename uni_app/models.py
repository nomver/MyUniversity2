from django.db import models
from django.contrib.auth import get_user_model

from django.conf import settings
User=settings.AUTH_USER_MODEL

class University(models.Model):
    name = models.CharField(max_length=250)
    address = models.TextField()

    class Meta:
        verbose_name = ("university")
        verbose_name_plural = ("universities")

    def __str__(self):
        return self.name


class Department(models.Model):
    name=models.CharField(max_length=200)
    university=models.ForeignKey(University,on_delete=models.CASCADE,)
    def __str__(self):
        return self.name
        
class Program(models.Model):
    name=models.CharField(max_length=200)
    department=models.ForeignKey(Department,related_name='dept_programs',on_delete=models.CASCADE)
    semester=models.PositiveIntegerField()
    
    def __str__(self):
        return str(self.name)+' '+str(self.semester)


class Subject(models.Model):
    title = models.CharField(max_length=200,)
    image = models.ImageField(upload_to='media/subjects/',null=True,blank=True)
    program = models.ForeignKey(Program,related_name='prog_subjects',on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    university=models.ForeignKey(University,related_name='uni_subjects',null=True,blank=True,on_delete=models.CASCADE)
    shortcourse=models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Lecture(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    subject = models.ForeignKey(
        Subject, related_name='lectures', on_delete=models.CASCADE,blank=True, null=True)
    title = models.CharField(max_length=50)
    audio = models.FileField(verbose_name="Video/Audio",upload_to='media/lectures/',null=True,blank=True)
    related_files = models.FileField(
        upload_to='media/lectures/related_files/', null=True, blank=True)
    completed = models.BooleanField(default=False)
    upload_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    students = models.ManyToManyField(
        User, related_name='completed_by', blank=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    teacher = models.ForeignKey(User, related_name='teacher_assignments', on_delete=models.CASCADE,blank=True,null=True)
    assignment=models.TextField()
    subject=models.ForeignKey(Subject, related_name='assignments',on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True,auto_now=False)
    due_on=models.DateTimeField()
    def __str__(self):
        return self.assignment


class SubmittedAssignment(models.Model):
    assignment=models.ForeignKey(Assignment, related_name='sub_assignments',on_delete=models.CASCADE)
    submitted_by=models.ForeignKey(User,related_name='sub_assignment',on_delete=models.PROTECT)
    submitted_docs=models.FileField(upload_to='media/assignments/',blank=True,null=True)
    submitted_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.submitted_by