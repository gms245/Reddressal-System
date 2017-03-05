from django.conf.urls import url,include
from .views import Login,home_student,home_staff,Logout,register,confirm,chat
from .models import UserProfile


app_name = 'accounts'



urlpatterns=[
    url(r'^home/student/$',home_student,name='home_student'),
    url(r'^home/staff/$',home_staff,name='home_staff'),
    url(r'^login/$',Login,name='login'),
    url(r'^logout/$',Logout,name='logout'),
    url(r'home/student/',include("student.urls")),
    url(r'home/staff/',include("staff.urls")),
    url(r'^register/$',register,name='register'),
    url(r'^confirm/(?P<activation_id>[\w-]+)/$',confirm,name='confirm'),
    url(r'^chat/$',chat,name='chat'),

]