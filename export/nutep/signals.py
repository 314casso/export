from nutep.models import HistoryMeta, UploadedTemplate
from django.db.models.signals import post_save
import datetime
from django.contrib.auth.models import User



def prepare_history(sender, instance, created, **kwargs): 
    if not hasattr(instance, 'user'):
        instance.user = User.objects.get(pk=1)   
    HistoryMeta.objects.create(date=datetime.datetime.now(), content_object=instance, is_created=created, user=instance.user)    
    

def connect_signals():
    post_save.connect(prepare_history, sender=UploadedTemplate)            