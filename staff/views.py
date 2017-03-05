from django.shortcuts import render,redirect
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Application,Files,UserProfile
from django.shortcuts import get_object_or_404
from student.forms import ApplicationForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage



@login_required(login_url='accounts:login')
def student_request(request):
	userProfile=UserProfile.objects.get(user=request.user)
	if userProfile.typ == 'Staff':
		apps=Application.objects.filter(originlwritertyp='Student').order_by('-id')
		papps = []
		for app in apps:
			if request.user.first_name in app.recievers:
				papps.append(app)
		return render(request,'staff_req.html',{'apps':papps})
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')

@login_required(login_url='accounts:login')
def staff_request(request):
	userProfile=UserProfile.objects.get(user=request.user)
	if userProfile.typ == 'Staff':
		apps=Application.objects.filter(originlwritertyp='Staff').order_by('-id')
		papps = []
		for app in apps:
			if request.user.first_name in app.recievers:
				papps.append(app)
		return render(request,'staff_req.html',{'apps':papps})
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')

@login_required(login_url='accounts:login')
def check(request,slug):
	userProfile=UserProfile.objects.get(user=request.user)
	if userProfile.typ == 'Staff':
		app=get_object_or_404(Application,slug=slug)
		recievers=app.recievers.split(';')  #doaa dosa  doaa
		length=len(recievers)  #3
		username=request.user.first_name #doaa
		for i in range(length):
			if recievers[length-i-1]==username:
				index=length-i-1  #0
				print (index)
				break
		if index!=0:
			reciever=recievers[index-1]
		else:
			reciever = 'None'
		replies = Application.objects.filter(parent=app.pk)
		# print(replies)
		# replies = replies.get(Q(writer=userProfile) | Q(reciever=request.user))
		originalwriter_=app.originalwriter
		lis=originalwriter_.split('@')
		originalwriter_=lis[0]
		print (originalwriter_)
		return render(request,'check.html',{'app':app,'replies':replies,'reciever':reciever,'index':index,'originalwriter_':originalwriter_})
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')

@login_required(login_url='accounts:login')
def create(request):
	userProfile=UserProfile.objects.get(user=request.user)
	if userProfile.typ == 'Staff':
		appform=ApplicationForm(request.POST or None)
		if request.method=='POST':
			if appform.is_valid():
				body=appform.cleaned_data.get("body")
				title=request.POST.get("title")
				dep=request.POST.get('dep')
				dean_pos=request.POST.get('dean-pos')
				dep_pos=request.POST.get('dep-pos')
				if dean_pos!='---------Choose the faculty---------':
					pos=dean_pos
				elif dep_pos!='---------Choose the faculty---------':
					pos=dep_pos
				reciever_ = UserProfile.objects.get(dep=dep,pos=pos)
				reciever = reciever_.user.email
				rc=User.objects.get(email=reciever)
				user_=UserProfile.objects.get(user=request.user)
				app=Application.objects.create(title=title,writer=user_,date=timezone.now(),
											body=body,recievers=rc.first_name,reciever=rc,
											originalwriter=request.user.username,
											originlwritertyp='Staff')
				for file in request.FILES.getlist("files"):
					file_ = Files(file=file,application=app)
					file_.save()
				messages.success(request,'Your application has been sent!')
				return redirect('accounts:login')
		return render(request,"student/appform.html",{'appform':appform})
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')


@login_required(login_url='accounts:login')
def reply(request,username,slug):
	userProfile=UserProfile.objects.get(user=request.user)
	if userProfile.typ == 'Staff':
		appform=ApplicationForm(request.POST or None)
		if request.method=='POST':
			if appform.is_valid():
				App=Application.objects.get(slug=slug)
				body=appform.cleaned_data.get("body")
				title=request.POST.get("title")
				reciever=User.objects.get(username=username)
				user_=UserProfile.objects.get(user=request.user)
				app=Application.objects.create(title=title,writer=user_,date=timezone.now(),
											body=body,recievers=reciever.first_name,reciever=reciever,
											originalwriter=request.user.username,
											originlwritertyp='Staff',parent=App.pk)
				for file in request.FILES.getlist("files"):
					file_ = Files(file=file,application=app)
					file_.save()
				messages.success(request,'Your reply has been successfully sent!')
				App.date = timezone.now()
				return redirect('accounts:login')
		return render(request,"replyform.html",{'appform':appform})
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')


@login_required(login_url='accounts:login')
def forward(request,slug):
	userProfile=UserProfile.objects.get(user=request.user)
	if userProfile.typ == 'Staff':
		app=get_object_or_404(Application,slug=slug)
		dep=request.POST.get('dep')
		pos=request.POST.get('pos')
		reciever_ = UserProfile.objects.get(dep=dep,pos=pos)
		reciever = reciever_.user.email
		rc=User.objects.get(email=reciever)
		app.recievers += ";"
		app.recievers += rc.first_name
		app.reciever = rc
		rc_profile=UserProfile.objects.get(user=request.user)
		app.writer=rc_profile
		app.date = timezone.now()
		app.save()
		# App=Application.objects.get(slug=slug)
		# App.pk=None
		# user=User.objects.get(email=reciever)
		# App.writer = UserProfile.objects.get(user=request.user)
		# App.reciever = user
		# App.slug=create_slug(App)
		# App.save()
		messages.success(request,'The application has been succesfully forwarded!')
		return redirect('accounts:login')
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')


@login_required(login_url='accounts:login')
def processed(request,slug):
	userProfile=UserProfile.objects.get(user=request.user)
	if userProfile.typ == 'Staff':
		app=get_object_or_404(Application,slug=slug)
		app.isprocessed = True
		app.date=timezone.now()
		app.save()
		return redirect('accounts:home_staff')
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')


@login_required(login_url='accounts:login')
def index(request):
	user_pr = get_object_or_404(UserProfile,user=request.user)
	if user_pr.typ == 'Staff':
		query = request.GET.get('query')
		if query:
			User = UserProfile.objects.get(user=request.user)
			app_qs = Application.objects.filter(originalwriter=request.user.username).order_by('-id').filter(title__icontains=query)
		else:
			User = UserProfile.objects.get(user=request.user)
			app_qs = Application.objects.filter(originalwriter=request.user.username,parent=0).order_by('-id')
		return render(request,'index1.html',{'app_qs':app_qs})
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')

@login_required(login_url='accounts:login')
def detail(request,slug):
	user_pr = get_object_or_404(UserProfile,user=request.user)
	if user_pr.typ == 'Staff':
		User = UserProfile.objects.get(user=request.user)
		try:
			App=Application.objects.get(slug=slug)
			replies=Application.objects.filter(parent=App.pk)
		except App.DoesNotExist():
			raise Http404
		recievers=list(App.recievers.split(";"))
		length=len(recievers)
		print (App.files_set.all())
		return render(request,'detail1.html',{'App':App,'recievers':recievers,'length':length,'replies':replies})
	else:
		messages.success(request,'url not found')
		return redirect('accounts:login')