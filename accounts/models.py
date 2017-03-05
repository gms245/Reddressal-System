from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.auth.models import User
 
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    typ = models.CharField(max_length=10)
    dep = models.CharField(max_length=30)
    pos = models.CharField(max_length=10)
    activation_key = models.CharField(max_length=40)
    def __str__(self):
        return self.user.username

class Application(models.Model):
    title = models.CharField(max_length=40,blank=True)
    body = models.TextField()
    recievers=models.TextField(default='None ')
    reciever=models.ForeignKey(User)
    writer = models.ForeignKey(UserProfile)
    # File = models.FileField(blank=True)
    date = models.DateTimeField()
    parent = models.IntegerField(default=0)
    slug=models.SlugField(unique=True,blank=True)
    isprocessed=models.BooleanField(default=False)
    originalwriter=models.CharField(max_length=40,default='originlwriter')
    originlwritertyp=models.CharField(max_length=10)
    def __str__(self):
        return self.title

class Files(models.Model):
    file=models.FileField()
    application=models.ForeignKey(Application)


def create_slug(instance,new_slug=None):
    slug=slugify(instance.title)
    if new_slug is not None:
        slug=new_slug
    qs= Application.objects.filter(slug=slug).order_by('-id')
    exists=qs.exists()
    if exists:
        new_slug="%s-%s" %(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_question_reciever(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_question_reciever,sender=Application)
        
