from django.conf.urls import url
from .views import writeapp,index,detail

app_name='student'

# Create your views here.
urlpatterns=[
	url(r'^create/$',writeapp,name='create'),
	url(r'^index/$',index,name='index'),
	# url(r'^inbox/$',inbox,name='inbox'),
	# url(r'^inbox/(?P<slug>[\w-]+)/$',inbox_detail,name='inbox_detail'),
	url(r'^index/(?P<slug>[\w-]+)/$',detail,name='detail'),
]