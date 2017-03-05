from django.conf.urls import url
from .views import student_request,staff_request,check,create,reply,forward,processed,index,detail

app_name='staff'

urlpatterns=[
	url(r'^student_req/$',student_request,name='student_request'),
	url(r'^staff_req/$',staff_request,name='staff_request'),
	url(r'^student_req/(?P<slug>[\w-]+)/$',check,name='check'),
	url(r'^staff_req/(?P<slug>[\w-]+)/$',check,name='check'),
	url(r'^staff/create/$',create,name='create'),
	url(r'^staff/reply/(?P<username>[\w-]+)/(?P<slug>[\w-]+)/$',reply,name='reply'),
	url(r'^staff/forward/(?P<slug>[\w-]+)/$',forward,name='forward'),
	url(r'^staff/processed/(?P<slug>[\w-]+)/$',processed,name='processed'),
	url(r'^staff/index/(?P<slug>[\w-]+)/$',detail,name='detail'),
	url(r'^staff/index/$',index,name='index'),
]
