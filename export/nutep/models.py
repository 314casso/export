# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_unicode
import datetime
import os
from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericForeignKey,\
    GenericRelation
from django.contrib.contenttypes.models import ContentType


def attachment_path(instance, filename):
    """
    Provide a file path that will help prevent files being overwritten, by
    putting attachments in a folder off attachments for id.
    """
    import os
    from django.conf import settings
    os.umask(0)
    path = 'attachments/%s_%s' % (datetime.date.today().month, datetime.date.today().year,)
    att_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(att_path):
        os.makedirs(att_path, 0777)
    return os.path.join(path, filename)

class BaseModelManager(models.Manager):    
    def get_query_set(self):
        return super(BaseModelManager, self).get_query_set().filter(deleted=False)

class ProcessDeletedModel(models.Model):
    objects = BaseModelManager()
    all_objects = models.Manager()
    deleted = models.BooleanField('Пометка удаления', default=False)
    class Meta:
        abstract = True 

class HistoryMeta(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')    
    is_created = models.BooleanField(default=False)    
    date = models.DateTimeField(blank=True, null=True, db_index=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)         
    
class UploadedTemplate(ProcessDeletedModel):
    NEW = 1
    INPROCESS = 2
    PROCESSED = 3
    ERROR = 500
    
    STATUS_CHOICES = (
        (NEW, force_unicode('Новый')),
        (INPROCESS, force_unicode('В обработке')),
        (PROCESSED, force_unicode('Обработан')),
        (ERROR, force_unicode('Ошибка')),     
    )
        
    attachment = models.FileField('Файл шаблона', upload_to=attachment_path) 
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW, db_index=True, blank=True)
    http_code = models.CharField('HTTP Код', max_length=50, null=True, blank=True)
    xml_response = models.TextField('XML ответ', null=True, blank=True)
    #Изменения
    history = GenericRelation('HistoryMeta')
    
    def last_event(self):
        if self.history:
            return self.history.all().order_by("-date")[:1].get()
    
    def __unicode__(self):
        return u'{0}'.format(self.attachment.name)  

    def filename(self):
        return os.path.basename(self.attachment.name)
    
    class Meta:
        verbose_name = force_unicode('Шаблон')
        verbose_name_plural = force_unicode('Шаблоны')
        ordering = ('-id', )
