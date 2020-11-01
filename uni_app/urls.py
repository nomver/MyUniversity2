from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
app_name = 'uni_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('listPrograms/',views.listPrograms,name='listPrograms'),
    path('subjects/', views.subjects, name='subjects'),
    path('<int:pk>/', views.listLectures, name='lectures'),
    path('lectures/<int:pk>/',views.lecture_detail,name='lecture_detail'),
    path('lecture/<int:pk>/', views.for_show_modal_audio, name='lectDetail'),
    path('lectures/<int:pk>/complete/',
         views.for_completion, name="for_completion"),

    path('addSubject/',views.addSubject,name='addSubject'),
    path('addShortCourse/',views.addShortCourse,name='addShortCourse'),
    path('addProgram/',views.addProgram,name='addProgram'),
    path('addLecture/<int:pk>/',views.addLecture,name='addLecture'),
    path('delete_lecture/<int:pk>/',views.delete_lecture,name='delete_lecture'),
    path('delete_subject/<int:pk>/',views.delete_subject,name='delete_subject'),
    path('add_assignment/<int:pk>/',views.add_assignment,name='add_assignment'),
    path('detail_assignment/<int:pk>/',views.detail_assignment,name='detail_assignment'),
    path('delete_assignment/<int:pk>/',views.delete_assignment,name='delete_assignment'),
    path('sub_assignment/<int:pk>/',views.sub_assignment,name='sub_assignment'),
    
    #hod Dashboard
    path('dashboard/',views.hod_dashboard,name='hod_dashboard'),
    path('programs/<int:pk>/', views.subjects, name='programs'),
]
