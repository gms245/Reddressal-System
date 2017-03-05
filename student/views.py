from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from accounts.models import Application,Files,UserProfile
from django.utils import timezone
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url='accounts:login')
def writeapp(request):
	user_pr = get_object_or_404(UserProfile,user=request.user)
	if user_pr.typ == 'Student':
		appform=ApplicationForm(request.POST or None)
		if request.method=='POST':
			if appform.is_valid():
				body=appform.cleaned_data.get("body")
				title=request.POST.get("title")
				dep=request.POST.get('dep')
				dean_pos=request.POST.get('dean-pos')
				dep_pos=request.POST.get('dep-pos')
				print (dean_pos)
				print (dep_pos)
				print (dep)
				if dean_pos!='---------Choose the faculty---------':
					pos=dean_pos
				elif dep_pos!='---------Choose the faculty---------':
					pos=dep_pos
				print(pos)
				reciever_ = get_object_or_404(UserProfile,dep=dep,pos=pos)
				reciever = reciever_.user.email
				rc=User.objects.get(email=reciever)
				user_=UserProfile.objects.get(user=request.user)
				app=Application.objects.create(title=title,writer=user_,date=timezone.now(),
											body=body,recievers=rc.first_name,reciever=rc,originalwriter=request.user.username,originlwritertyp='Student')
				for file in request.FILES.getlist("files"):
					file_ = Files(file=file,application=app)
					file_.save()
				messages.success(request,'Your grievance/request has been sent!')
				return redirect('accounts:login')
		return render(request,"student/appform.html",{'appform':appform})
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')


@login_required(login_url='accounts:login')
def index(request):
	user_pr = get_object_or_404(UserProfile,user=request.user)
	if user_pr.typ == 'Student':
		query = request.GET.get('query')
		if query:
			User = UserProfile.objects.get(user=request.user)
			app_qs = Application.objects.filter(originalwriter=request.user.username).order_by('-id').filter(title__icontains=query)
		else:
			User = UserProfile.objects.get(user=request.user)
			app_qs = Application.objects.filter(originalwriter=request.user.username).order_by('-id')
		return render(request,'student/index.html',{'app_qs':app_qs})
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')


@login_required(login_url='accounts:login')
def detail(request,slug):
	user_pr = get_object_or_404(UserProfile,user=request.user)
	if user_pr.typ == 'Student':
		User = UserProfile.objects.get(user=request.user)
		try:
			App=Application.objects.get(slug=slug)
			replies=Application.objects.filter(parent=App.pk)
		except App.DoesNotExist():
			raise Http404
		recievers=list(App.recievers.split(";"))
		length=len(recievers)
		print (App.files_set.all())
		return render(request,'student/detail.html',{'App':App,'recievers':recievers,'length':length,'replies':replies})
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')


# @login_required(login_url='accounts:login')
# def inbox(request):
# 	user_pr = get_object_or_404(UserProfile,user=request.user)
# 	if user_pr.typ == 'Student':
# 		apps=Application.objects.filter(reciever=request.user).order_by('-id')
# 		return render(request,'student/inbox.html',{'apps':apps})
# 	else:
# 		messages.success(request,'url not found')
# 		return redirect('accounts:login')


# @login_required(login_url='accounts:login')
# def inbox_detail(request,slug):
# 	user_pr = get_object_or_404(UserProfile,user=request.user)
# 	if user_pr.typ == 'Student':
# 		app=get_object_or_404(Application,slug=slug)
# 		print (app)
# 		return render(request,'student/inbox_detail.html',{'app':app})
# 	else:
# 		messages.success(request,'url not found')
# 		return redirect('accounts:login')


