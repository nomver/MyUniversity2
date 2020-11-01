from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
# from django.urls import 
from .forms import ProfileStudentForm,ProfileTeacherForm,UserCreateForm,ProfileHodForm
from accounts import models
from django.http import JsonResponse
from django.template.loader import render_to_string
# Create your views here.
@login_required
def update_profile(request):
    if request.user.you_are=='Teacher':
        form=ProfileTeacherForm(instance=request.user.user_profile)
    elif request.user.is_hod:
        form=ProfileHodForm(instance=request.user.user_profile)
    else:
        form=ProfileStudentForm(instance=request.user.user_profile)
    
    if request.method=='POST':
        
        if request.user.you_are=='Teacher':
            form=ProfileTeacherForm(request.POST,instance=request.user.user_profile)
        else:
            form=ProfileStudentForm(request.POST,instance=request.user.user_profile)
        if form.is_valid():
            form1=form.save(commit=False)
            form1.user=request.user
            if request.FILES.get('profile_image'):
                form1.profile_image=request.FILES['profile_image']
            form1.save()
            return redirect('uni_app:subjects')
    else:
        return render(request,'accounts/ProfileUpdate.html',{'form':form})


def signup(request):
    form=UserCreateForm()
    if request.method=='POST':
        form=UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    return render(request,'accounts/signup.html',{'form':form})



from accounts import forms
@login_required
def UserView(request,pk):
    student=get_object_or_404(models.User,pk=pk)
    if student.is_student:
        if request.user.is_teacher:
            message_form=forms.MessageForm()
            return render(request,'accounts/UserView.html',{'student':student,'message_form':message_form})
    
    if request.user.is_hod:
        message_form=forms.MessageForm()
        return render(request,'accounts/UserView.html',{'student':student,'message_form':message_form})
    return redirect('/')

def delete_user(request, pk):
    teacher=get_object_or_404(models.User,pk=pk)
    if request.user.is_hod:
        if request.user==teacher:
            return redirect('uni_app:hod_dashboard')
        teacher.delete()
        return redirect('uni_app:hod_dashboard')
    elif request.user.is_teacher:
        if teacher.is_student:
            teacher.delete()
            return redirect('uni_app:subjects')
        else:
            return JsonResponse({'msg':'You cant delete a teacher please contact to hod.'})
    else:
        return JsonResponse({'msg':'you are not allowed!'})    

@login_required
def msg_to_student(request,pk):
    student=get_object_or_404(models.User,pk=pk)
    form=forms.MessageForm()
    if request.user.is_hod or request.user.is_teacher:
        if request.method=='POST':
            form=forms.MessageForm(request.POST)
            if form.is_valid():
                form1=form.save(commit=False)
                form1.from_teacher=request.user
                form1.to_student=student
                form1.save()
                return redirect(reverse_lazy('accounts:UserView',kwargs={'pk':pk}))
    else:
        return redirect('uni_app:subjects')


@login_required
def msgToAll(request):
    form=forms.MessageForm()
    data=dict()
    if request.user.is_hod:
        dept=request.user.department
        uni=request.user.university
        teachers=models.User.objects.filter(is_teacher=True,department=dept,university=uni)
        if request.method=='POST':
            for teacher in teachers:
                print(request.user,"---------",request.POST['message'],"-------------",teacher)
                models.MessageToUser.objects.create(message=request.POST['message'],from_teacher=request.user,to_student=teacher)
            return redirect('uni_app:hod_dashboard')
        else:
            data['d']=render_to_string('accounts/sendMessage.html',{'form':form},request=request)
            return JsonResponse(data)
    else:
        return JsonResponse({'msg':'you are not allowed!'})

@login_required
def msg_detail(request,pk):
    msg=get_object_or_404(models.MessageToUser,pk=pk)
    data=dict()
    data['msg1']=render_to_string('accounts/msg_detail.html',{'msg':msg})
    return JsonResponse(data)

@login_required
def delete_msg(request,pk):
    msg=get_object_or_404(models.MessageToUser,pk=pk)
    msg.delete()
    return redirect('uni_app:subjects')

@login_required
def approve_teacher(request, pk):
    teacher=get_object_or_404(models.User,pk=pk)
    if request.user.is_hod:
        if teacher.department==request.user.department:
            teacher.is_teacher=True
            teacher.save()
            return redirect(reverse_lazy('accounts:UserView',kwargs={'pk':pk}))
    else:
        return JsonResponse({'msg':'Only Hod of this department is allowed!'})