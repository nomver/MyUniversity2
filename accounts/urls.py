from django.urls import path,include
from . import views
app_name='accounts'


urlpatterns=[
    path('update_profile/',views.update_profile,name="update_profile"),
    path('signup/',views.signup,name='signup'),
    path('',include('django.contrib.auth.urls')),
    path('user/<int:pk>/',views.UserView,name='UserView'),
    path('msgTo/<int:pk>/',views.msg_to_student,name='msgToStudent'),
    path('msgToAll/',views.msgToAll,name='msgToAll'),
    path('approve_teacher/<int:pk>/',views.approve_teacher,name='approve_teacher'),
    path('delete_user/<int:pk>/',views.delete_user,name='delete_user'),
    path('msg_detail/<int:pk>/',views.msg_detail,name='msg_detail'),
    path('delete_msg/<int:pk>/',views.delete_msg,name='delete_msg'),
]