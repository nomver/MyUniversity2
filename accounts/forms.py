from django import forms
from .models import Profile,MessageToUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User=get_user_model()


class ProfileStudentForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_image','program','Rollnumber',]


        widgets={
            'university':forms.Select(attrs={'required':'required'}),
            'Rollnumber':forms.NumberInput(attrs={'required':'required','type':'number','min':"0"})
        }

class ProfileTeacherForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_image','CNIC_number']

        widgets={
            'profile_image':forms.FileInput(attrs={'required':'required','accept':"image/*"}),
            'CNIC_number':forms.NumberInput(attrs={'required':'required','type':'number','min':"0"}),
        }
        
class ProfileHodForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_image',]

        widgets={
            'profile_image':forms.FileInput(attrs={'required':'required','accept':"image/*"}),
            
        }

class UserCreateForm(forms.Form,UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','you_are','university','department','password1','password2',]



class MessageForm(forms.ModelForm):
    class Meta:
        model=MessageToUser
        fields=['message',]

