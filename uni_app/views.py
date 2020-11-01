from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse_lazy
from . import models
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from uni_app import forms
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your views here.


def home(request):
    return render(request,'uni_app/home.html',)

@login_required
def subjects(request, pk=None):
    program=''
    programs=''
    # lectures=models.Lecture.objects.all()
    if not pk:
        user_prgrm = request.user.user_profile.program
        user_uni=request.user.university
        subjects = models.Subject.objects.filter(program=user_prgrm).filter(university=user_uni)
        if request.user.is_teacher or request.user.is_hod:
            subjects=models.Subject.objects.filter(teacher=request.user)
    if pk:
        if request.user.is_hod or request.user.is_teacher:
            program=get_object_or_404(models.Program,pk=pk)
            subjects=models.Subject.objects.filter(program=program)
        else:
            return redirect('uni_app:subjects')
    return render(request, 'uni_app/subjects.html', {'subjects': subjects,'program':program,'programs':programs})

@login_required
def listPrograms(request):
    if request.user.you_are == 'Student':
        return redirect('uni_app:subjects')
    department=request.user.department
    programs=models.Program.objects.filter(department=request.user.department)
    return render(request,'uni_app/all_programs.html',{'programs':programs}) 

@login_required
def hod_dashboard(request,pk=None):
    if request.user.is_hod or request.user.you_are=='Teacher':
        user_dept=request.user.department
        programs=models.Program.objects.filter(department=user_dept)
        teachers=User.objects.filter(is_teacher=True).filter(department=user_dept)
        req_teachers=User.objects.filter(you_are='Teacher',is_teacher=False).filter(department=user_dept)
        return render(request,'uni_app/hodDashboard.html',{'req_teachers':req_teachers,'programs':programs,'teachers':teachers})
    
    return redirect('uni_app:subjects')

@login_required
def listLectures(request, pk):
    subject = get_object_or_404(models.Subject, pk=pk)
    lectures = models.Lecture.objects.filter(subject__pk=subject.pk)
    completed_lect = []
    uncomplete_lect = []
    for lect in lectures:
        if request.user in lect.students.all():
            completed_lect.append(lect)
        else:
            uncomplete_lect.append(lect)

    return render(request, 'uni_app/lectures.html', {'subject': subject, 'completed_lect': completed_lect, 'uncomplete_lect': uncomplete_lect})


def for_show_modal_audio(request, pk):
    data = dict()
    lecture = get_object_or_404(models.Lecture, pk=pk)
    data['LectFromView'] = render_to_string(
        'uni_app/lecture_detail.html', {'lecture': lecture})
    return JsonResponse(data)


def for_completion(request, pk):
    data = dict()
    lecture = get_object_or_404(models.Lecture, pk=pk)
    lecture.completed = True
    lecture.students.add(request.user)
    lecture.save()
    data['reverseUrl'] = lecture.subject.pk
    if request.user not in lecture.students.all():
        data['message'] = 'You Completed "{}". Your next lecture is unlocked'.format(
            lecture.title)
    return JsonResponse(data)


@login_required
def addProgram(request):
    form=forms.AddProgramForm()
    if request.user.is_authenticated:
        if request.user.is_hod:
            if request.method=='POST':
                form=forms.AddProgramForm(request.POST)
                if form.is_valid():
                    form1=form.save(commit=False)
                    form1.department=request.user.department
                    form1.save()
                    return redirect('uni_app:hod_dashboard')
                else:
                    print("form error")
            else:
                return render(request,'uni_app/addProgram.html',{'form':form})

        else:
            return render(request,'uni_app/addProgram.html',{'form':form,'errors':'Sorry You are not hod!'})
    else:
        return redirect('accounts:login')


@login_required
def addSubject(request):
    form=forms.AddSubjectForm()
    if request.user.is_authenticated:
        if request.user.is_teacher:
            if request.method=='POST':
                form=forms.AddSubjectForm(request.POST)
                if form.is_valid():
                    form1=form.save(commit=False)
                    form1.teacher=request.user
                    form1.university=request.user.university
                    if request.FILES:
                        form1.image=request.FILES['image']
                    form1.save()
                    return redirect('uni_app:subjects')
                else:
                    print("form error")
            else:
                return render(request,'uni_app/addSubject.html',{'form':form})

        else:
            return render(request,'uni_app/addSubject.html',{'form':form,'error':'Sorry You are not teacher!'})
    else:
        return redirect('accounts:login')

@login_required
def addShortCourse(request):
    form=forms.AddSubjectForm()
    if request.user.is_authenticated:
        if request.user.is_teacher:
            if request.method=='POST':
                form=forms.AddSubjectForm(request.POST)
                if form.is_valid():
                    form1=form.save(commit=False)
                    form1.shortcourse=True
                    form1.teacher=request.user
                    form1.university=request.user.university
                    if request.FILES:
                        form1.image=request.FILES['image']
                    form1.save()
                    return redirect('uni_app:subjects')
                else:
                    print("form error")
            else:
                return render(request,'uni_app/addSubject.html',{'form':form,'msg':'A Short Course'})

        else:
            return render(request,'uni_app/addSubject.html',{'form':form,'error':'Sorry You are not teacher!','msg':'A Short Course'})
    else:
        return redirect('accounts:login')

@login_required
def addLecture(request,pk):
    subject=get_object_or_404(models.Subject,pk=pk)
    form=forms.AddLectureForm()
    if request.user.is_teacher:
        if request.method=='POST':
            form=forms.AddLectureForm(request.POST)
            if form.is_valid():
                form1=form.save(commit=False)
                form1.teacher=request.user
                form1.subject=subject
                if request.FILES['audio']:
                    form1.audio=request.FILES['audio']
                if request.FILES.get('related_files'):
                    form1.related_files=request.FILES['related_files']
                form1.save()
                form1.students.add(request.user)
                return redirect(reverse_lazy('uni_app:lectures',kwargs={'pk':pk}))
            else:
                return render(request,'uni_app/addLecture.html',{'subject':subject,'form':form,'errors':forms.errors})
        else:
            return render(request,'uni_app/addLecture.html',{'subject':subject,'form':form})
    return render(request,'uni_app/addLecture.html',{'form':form,'error':'you are not a teacher!'})


@login_required
def lecture_detail(request, pk):
    lecture=get_object_or_404(models.Lecture, pk=pk)
    return render(request,'uni_app/lecture.html',{'lecture':lecture})

@login_required
def delete_subject(request,pk):
    subject=get_object_or_404(models.Subject,pk=pk)
    if request.user == subject.teacher or request.user.is_hod:
        subject.delete()
        return redirect(reverse_lazy('uni_app:subjects'))
    else:
        return JsonResponse({'msg':'you are not allowed'})

@login_required
def delete_lecture(request,pk):
    lecture=get_object_or_404(models.Lecture,pk=pk)
    sub_pk=lecture.subject.pk
    print(sub_pk,'--------------------------')
    if request.user == lecture.teacher:
        lecture.delete()
        return redirect(reverse_lazy('uni_app:lectures',kwargs={'pk':sub_pk}))

    else:
        return JsonResponse({'msg':'you are not allowed'})


@login_required
def add_assignment(request,pk):
    subject=get_object_or_404(models.Subject,pk=pk)
    if request.user.username == subject.teacher.username:
        form=forms.AddAssignmentForm()
        if request.method=='POST':
            form=forms.AddAssignmentForm(request.POST)
            if form.is_valid():
                form1=form.save(commit=False)
                form1.teacher=request.user
                form1.subject=subject
                form1.save()
                return redirect(reverse_lazy('uni_app:lectures',kwargs={'pk':subject.pk}))
        else:
            return render(request,'uni_app/add_assignment.html',{'form':form,'subject':subject})
    else:
        return JsonResponse({'msg':'you are not allowed!'})

from django.utils import timezone
@login_required
def detail_assignment(request, pk):
    assignment=get_object_or_404(models.Assignment,pk=pk)
    submitted_assignments=models.SubmittedAssignment.objects.filter(assignment=assignment)

    if timezone.now().date() <= assignment.due_on.date():
        if request.method=='POST':
            form=forms.SubmittedAssignmentForm(request.POST)
            if form.is_valid():
                form1=form.save(commit=False)
                form1.submitted_by=request.user
                form1.assignment=assignment
                if request.FILES['submitted_docs']:
                    form1.submitted_docs=request.FILES['submitted_docs']
                form1.save()
                return redirect(reverse_lazy('uni_app:detail_assignment',kwargs={'pk':pk}))
        else:
            form=forms.SubmittedAssignmentForm()
    else:
        form=''
    return render(request,'uni_app/detail_assignment.html',{'submitted_assignments':submitted_assignments,'assignment':assignment,'form':form})


@login_required
def delete_assignment(request, pk):
    assignment=get_object_or_404(models.Assignment,pk=pk)
    sub_pk=assignment.subject.pk
    if assignment.teacher==request.user:
        assignment.delete()
        return redirect('uni_app:lectures',kwargs={'pk':sub_pk })
    else:
        return JsonResponse({'msg':'you are not allowed!'})

@login_required
def sub_assignment(request, pk):
    sub_assignment=get_object_or_404(models.SubmittedAssignment,pk=pk)
    return render(request,'uni_app/sub_assignment.html',{'sub_assignment':sub_assignment})