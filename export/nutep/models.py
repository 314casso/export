# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import force_unicode
import datetime
import os
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,\
    GenericRelation
from nutep.middleware import get_current_user



def attachment_path(instance, filename):    
    from django.conf import settings
    os.umask(0)
    path = 'attachments/%s_%s' % (datetime.date.today().month, datetime.date.today().year,)
    att_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(att_path):
        os.makedirs(att_path, 0777)
    return os.path.join(path, filename)


class BaseModelManager(models.Manager):    
    def get_queryset(self):
        #print get_current_user()
        return super(BaseModelManager, self).get_queryset().filter(deleted=False)


class ProcessDeletedModel(models.Model):    
    objects = BaseModelManager()
    all_objects = models.Manager()
    deleted = models.BooleanField('Пометка удаления', default=False)
    def last_event(self):
        if self.history:
            return self.history.all().order_by("-date")[:1].get()
    class Meta:
        abstract = True 


class BaseModel(ProcessDeletedModel):
    name = models.CharField('Наименование', max_length=150, db_index=True)
    guid = models.CharField(max_length=50, null=True, db_index=True)
    class Meta:
        abstract = True


class HistoryMeta(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')    
    is_created = models.BooleanField(default=False)    
    date = models.DateTimeField(blank=True, null=True, db_index=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)         
    

class BaseError(models.Model):
    XML = 1
    MODEL = 2
    UNKNOWN = 3 
    WEBFAULT = 4   
    
    TYPE_CHOICES = (
        (XML, force_unicode('Ошибка учетной системы')),
        (WEBFAULT, force_unicode('Ошибка обмена данных')),
        (MODEL, force_unicode('Ошибка данных')),
        (UNKNOWN, force_unicode('Ошибка')),
             
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')   
    date = models.DateTimeField(auto_now_add=True, blank=True)
    code = models.CharField(max_length=50, db_index=True, blank=True, null=True)
    field = models.CharField(max_length=50, db_index=True, blank=True, null=True)            
    message = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=UNKNOWN, db_index=True, blank=True)
    
    def __unicode__(self):
        return u'{0}'.format(self.code) 
    class Meta:
        verbose_name = force_unicode('Ошибка')
        verbose_name_plural = force_unicode('Ошибки')
        ordering = ('id', )
    

class Vessel(BaseModel):
    history = GenericRelation('HistoryMeta')
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:        
        verbose_name = force_unicode('Судно')
        verbose_name_plural = force_unicode('Суда')
        ordering = ('name', )
    
    
class Voyage(BaseModel):        
    vessel = models.ForeignKey(Vessel, null=True, related_name="voyages")
    flag = models.CharField(max_length=100, null=True, blank=True) 
    etd = models.DateTimeField(null=True, blank=True)
    history = GenericRelation('HistoryMeta')
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('Рейс')
        verbose_name_plural = force_unicode('Рейсы')
        ordering = ('name', )
    
    
class Line(BaseModel):        
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('Линия')
        verbose_name_plural = force_unicode('Линии')
        ordering = ('name', )
        
        
class Terminal(BaseModel):        
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('Терминал')
        verbose_name_plural = force_unicode('Терминалы')
        ordering = ('name', )           
  

class UserProfile(models.Model):
    guid = models.CharField(max_length=50,null=True)
    user = models.OneToOneField(User, unique=True, related_name='profile')
    lines = models.ManyToManyField(Line)


class Draft(models.Model):
    name = models.CharField('BL', max_length=150, db_index=True)        
    guid = models.CharField(max_length=50)        
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)    
    date = models.DateTimeField()
    shipper = models.CharField(max_length=255, null=True, blank=True)
    consignee = models.CharField(max_length=255, null=True, blank=True)    
    voyage = models.ForeignKey(Voyage, related_name="drafts", null=True)
    finalDestination = models.CharField(max_length=255, null=True, blank=True)
    POD = models.CharField(max_length=150, null=True, blank=True)
    POL = models.CharField(max_length=150, null=True, blank=True)
    finstatus = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    poruchenie = models.BooleanField(default=False)
    poruchenieNums = models.CharField(max_length=150, null=True, blank=True)
    notify = models.CharField(max_length=255, null=True, blank=True)
    line = models.ForeignKey(Line)
    template = models.ForeignKey("UploadedTemplate", related_name='drafts')
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('Коносамент')
        verbose_name_plural = force_unicode('Коносаменты')
        ordering = ('name', )  
            
            
class Container(models.Model):
    name = models.CharField(max_length=12, db_index=True)
    SOC = models.BooleanField(default=False)
    size = models.CharField(max_length=2, db_index=True)
    type = models.CharField(max_length=3, db_index=True)
    line = models.ForeignKey(Line, null=True, blank=True)
    seal = models.CharField(max_length=150, null=True, blank=True)
    cargo = models.CharField(max_length=255, null=True, blank=True)
    netto = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=3)
    gross = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=3)
    tare = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=3)
    package = models.CharField(max_length=150, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    draft = models.ForeignKey(Draft, related_name="containers", on_delete=models.CASCADE)
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('Контейнер')
        verbose_name_plural = force_unicode('Контейнеры')
        ordering = ('name', ) 
                              

class Readiness(models.Model):
    size = models.CharField(max_length=2, db_index=True)
    type = models.CharField(max_length=3, db_index=True)
    ordered = models.PositiveIntegerField(null=True, blank=True)
    done = models.PositiveIntegerField(null=True, blank=True)
    draft = models.ForeignKey(Draft, related_name="readiness", on_delete=models.CASCADE)
    def __unicode__(self):
        return u'{0}'.format(self.id) 
    class Meta:
        verbose_name = force_unicode('Готовность')
        verbose_name_plural = force_unicode('Готовность')
        ordering = ('id', ) 

class Contract(BaseModel):    
    line = models.ForeignKey(Line, related_name="contracts")
    terminal = models.ForeignKey(Terminal)
    startdate = models.DateTimeField(db_index=True)
    expired = models.DateTimeField(db_index=True)
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('Договор')
        verbose_name_plural = force_unicode('Договоры')
        ordering = ('name', )
    
    
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
    voyage = models.ForeignKey(Voyage, blank=True, null=True, on_delete=models.PROTECT, related_name="templates")
    contract = models.ForeignKey(Contract, blank=True, null=True, on_delete=models.PROTECT)
    
    history = GenericRelation('HistoryMeta')
    
    errors = GenericRelation('BaseError')
    
    def drafts_done(self):        
        return self.drafts.filter(poruchenie=True)    
        
    def drafts_total(self):        
        return self.drafts.all()
        
    def drafts_readiness(self):        
        total = float(len(self.drafts_total()))
        if not total:
            return 0
        done = float(len(self.drafts_done()))        
        return int(done / total * 100)        
    
    def set_status(self):
        if len(self.errors.all()):
            self.status = UploadedTemplate.ERROR
        elif self.drafts_readiness() == 100:            
            self.status = UploadedTemplate.PROCESSED
        else:
            self.status = UploadedTemplate.INPROCESS
        self.save()
    
    def __unicode__(self):
        return u'{0}'.format(self.attachment.name)  

    def filename(self):
        return os.path.basename(self.attachment.name)
    
    def status_class(self):
        mapper = {
                 self.NEW : 'new',
                 self.PROCESSED : 'success',
                 self.INPROCESS : 'info',
                 self.ERROR : 'danger',
                 }
        return mapper.get(self.status)
    
    class Meta:
        verbose_name = force_unicode('Шаблон')
        verbose_name_plural = force_unicode('Шаблоны')
        ordering = ('-id', )
