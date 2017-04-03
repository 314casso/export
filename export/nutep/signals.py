from nutep.models import HistoryMeta, UploadedTemplate, Voyage, Vessel, Line
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.timezone import now 


def prepare_history(sender, instance, created, **kwargs): 
    if not hasattr(instance, 'user'):
        instance.user = User.objects.get(pk=1)   
    HistoryMeta.objects.create(date=now(), content_object=instance, is_created=created, user=instance.user)    
    

def connect_signals():
    post_save.connect(prepare_history, sender=UploadedTemplate)            
    post_save.connect(prepare_history, sender=Voyage)
    post_save.connect(prepare_history, sender=Vessel)
    post_save.connect(prepare_history, sender=Line)