# -*- coding: utf-8 -*-
import base64

from django.apps import apps
from django.contrib.auth.models import User
from suds.cache import NoCache
from suds.client import Client

from nutep.models import (BaseError, Container, Contract, Draft, Line,
                          Readiness, UploadedTemplate, Voyage)


class BaseService(object):
    username = None
    password = None
    url = None
    def __init__(self, settings):
        self.set_client(settings)
            
    def set_client(self, settings):
        for key in settings.iterkeys():             
            setattr(self, key, settings.get(key))   
        base64string = base64.encodestring(
            '%s:%s' % (self.username, self.password)).replace('\n', '')
        authenticationHeader = {
            "SOAPAction" : "ActionName",
            "Authorization" : "Basic %s" % base64string
        } 
        self._client = Client(self.url, headers=authenticationHeader, cache=NoCache(), timeout=500)        
                                     

class DraftService(BaseService):       
    def get_voyage(self, xml_voyage):
        vessel = self.get_value('Vessel', xml_voyage.vessel)        
        model = Voyage
        xml_value = xml_voyage
        try:
            value = model.objects.get(guid=xml_value.guid,)
        except model.DoesNotExist:
            value = None
        if not value:
            q = model.objects.filter(name=xml_value.name, vessel=vessel, guid__isnull=True)
            if q:
                value = q.first()
                value.guid = xml_value.guid        
                value.save()       
        if not value:                      
            value = model.objects.create(guid=xml_value.guid,)
            value.name = xml_value.name
            value.vessel = vessel
            value.etd = xml_value.etd
            value.guid = xml_value.guid        
            value.save()        
        return value
    
    def get_line(self, xml_line):         
        line, created = Line.objects.get_or_create(guid=xml_line.guid,)  # pylint: disable=W0612
        line.name = xml_line.name        
        line.guid = xml_line.guid
        line.save()        
        return line
    
    def get_value(self, model_name, xml_value):
        model = apps.get_model(app_label='nutep', model_name=model_name)
        try:
            value = model.objects.get(guid=xml_value.guid,)
        except model.DoesNotExist:
            value = None
        if not value:
            q = model.objects.filter(name=xml_value.name, guid__isnull=True)
            if q:
                value = q.first()
                value.guid = xml_value.guid        
                value.save()       
        if not value:                      
            value = model.objects.create(guid=xml_value.guid,)
            value.name = xml_value.name
            value.guid = xml_value.guid        
            value.save()        
        return value
    
    def get_vessel(self, xml_vessel):             
        return self.get_value('Vessel', xml_vessel)
    
    def get_contract(self, xml_contract):         
        contract, created = Contract.objects.get_or_create( # pylint: disable=W0612
            guid=xml_contract.guid,)  
        contract.name = xml_contract.name
        contract.guid = xml_contract.guid        
        contract.save()        
        return contract

    def load_draft(self, template, user):
        xml_template = self._client.factory.create('Template')
        xml_template.id = template.id
        xml_template.userguid = user.profile.guid
        xml_template.contractguid = template.contract.guid         
        xml_template.data = template.attachment.read().encode('base64')                
        response = self._client.service.LoadDraft(xml_template)                
        self.parse_response(response, template)
        return response
                        
    def update_status(self, pk, user): 
        template = UploadedTemplate.objects.get(pk=pk)
        template.user = user 
        if template.errors.all():
            raise Exception(u"Шаблон содержит ошибки, обновление новозможно")
        response = self._client.service.GetStatus(pk)      
        self.parse_response(response, template)
        return response
    
    def parse_response(self, response, template):
        self.delete_data(template)    
        if response.errors:
            fields = ['code', 'error', 'message']
            for xml_error in response.errors.error:                  
                base_error = BaseError()
                for field in fields:
                    value = u'%s' % xml_error[field] if field in xml_error else None                        
                    setattr(base_error, field, value)                
                base_error.content_object = template
                base_error.type = BaseError.XML
                base_error.save()
        
        if template.errors.all():
            template.set_status()
            return response
        
        voyage = self.get_voyage(response.voyage)
        template.voyage = voyage 
        template.contract = self.get_contract(response.contract)
        template.xml_response = response
        template.save()  
        if response.drafts:      
            for xml_draft in response.drafts.draft:            
                draft = Draft()
                fields = ['name', 'guid', 'date', 'shipper', 'consignee', 'finalDestination',
                          'POD', 'POL', 'finstatus', 'status', 'poruchenie', 'poruchenieNums', 'notify']
                for field in fields:
                    value = u'%s' % xml_draft[field] if xml_draft[field] else xml_draft[field]                        
                    setattr(draft, field, value)                
                draft.user = User.objects.get(profile__guid=xml_draft.userguid)                                
                draft.voyage = self.get_voyage(xml_draft.voyage) 
                draft.line = self.get_line(xml_draft.line)
                draft.template = template               
                draft.save()
                fields = ['name', 'SOC', 'size', 'type', 'seal', 'cargo',
                          'netto', 'gross', 'tare', 'package', 'quantity']
                for xml_container in xml_draft.containers.container:
                    container = Container()
                    for field in fields:
                        value = u'%s' % xml_container[field] if xml_container[field] else xml_container[field]
                        setattr(container, field, value)
                    container.line = self.get_line(xml_container.line)
                    container.draft = draft
                    container.save()
                fields = ['size', 'type', 'ordered', 'done', ]
                for xml_readiness in xml_draft.readiness.row:
                    readiness = Readiness()
                    for field in fields:                    
                        setattr(readiness, field, xml_readiness[field])                
                    readiness.draft = draft
                    readiness.save()
        template.set_status()
        
            
    def delete_data(self, template):        
        drafts = Draft.objects.filter(template=template)
        drafts.delete()
        template.errors.all().delete()
   
class TemplateException(Exception):
    pass   
        
class ExcelHelper(object):    
    @staticmethod            
    def get_value(ws, col_name, required=False):
        cell = ExcelHelper.get_cell(ws, col_name)
        value = ExcelHelper.get_cell_value(ws, cell)
        if required and not value:
            raise TemplateException(u'Столбец %s не может быть пустым' % col_name) 
        return value
            
    @staticmethod
    def get_cell(ws, col_name):        
        for row in ws.iter_rows(min_row=1, max_col=ws.max_column, max_row=ws.max_row):               
            for cell in row:
                cval = u'%s' % cell.value
                if cell.value and cval.upper() == col_name.upper():
                    return cell
        raise TemplateException(u'Столбец %s не найден' % col_name) 
        
    @staticmethod            
    def get_cell_value(ws, cell):
        rng = "%s%s:%s%s" % (cell.column, int(cell.row) + 1,
                             cell.column, int(cell.row) + 1)
        result = set() 
        for row in ws.iter_rows(rng):
            result.add(row[0].value)            
        if len(result) == 1:
            return result.pop()
        elif len(result) == 0:
            raise TemplateException(u'Столбец %s не заполнен' % cell.value)               
        else:
            raise TemplateException(u'Столбец %s содержит более одного рейса %s' % (cell.value, u','.join(result)))  
