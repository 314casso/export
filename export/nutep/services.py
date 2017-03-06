# -*- coding: utf-8 -*-
from suds.client import Client
from __builtin__ import setattr
import base64
from suds.cache import NoCache
from nutep.models import Draft, UploadedTemplate, Voyage, Line, Vessel,\
    Contract, Container, Readiness
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode


class BaseService():
    def __init__(self, settings):
        self.set_client(settings)
            
    def set_client(self, settings):
        for key in settings.iterkeys():             
            setattr(self, key, settings.get(key))   
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        authenticationHeader = {
            "SOAPAction" : "ActionName",
            "Authorization" : "Basic %s" % base64string
        }                
        self._client = Client(self.url, headers=authenticationHeader, cache=NoCache())        
        

class DraftService(BaseService):       
    def get_voyage(self, xml_voyage):         
        voyage, created = Voyage.objects.get_or_create(name=xml_voyage.name,)  # @UnusedVariable
        if created or not voyage.guid:        
            voyage.name = xml_voyage.name
            voyage.guid = xml_voyage.guid 
            voyage.etd = xml_voyage.etd
            voyage.vessel = self.get_vessel(xml_voyage.vessel)         
            voyage.save()        
        return voyage
    
    def get_line(self, xml_line):         
        line, created = Line.objects.get_or_create(guid=xml_line.guid,)  # @UnusedVariable
        if created or not line.guid:        
            line.name = xml_line.name        
            line.guid = xml_line.guid
            line.save()        
        return line
    
    def get_vessel(self, xml_vessel):         
        vessel, created = Vessel.objects.get_or_create(guid=xml_vessel.guid,)  # @UnusedVariable
        if created or not vessel.guid:        
            vessel.name = xml_vessel.name
            vessel.guid = xml_vessel.guid        
            vessel.save()        
        return vessel
    
    def get_contract(self, xml_contract):         
        contract, created = Contract.objects.get_or_create(guid=xml_contract.guid,)  # @UnusedVariable
        if created or not xml_contract.guid:        
            contract.name = xml_contract.name
            contract.guid = xml_contract.guid        
            contract.save()        
        return contract

    def load_draft(self, template, user):
        xml_template = self._client.factory.create('Template')
        xml_template.id = template.id
        xml_template.userguid = user.get_profile().guid        
        xml_template.data = template.attachment.read().encode('base64')
                
        response = self._client.service.LoadDraft(xml_template)
        print response        
        #self.parse_response(response, template.id)
        return response
                        
    def update_status(self, pk):
        response = self._client.service.GetStatus(pk)      
        self.parse_response(response, pk)
        return response
    
    def parse_response(self, response, pk):
        voyage = self.get_voyage(response.voyage)
        template = UploadedTemplate.objects.get(pk=pk)
        template.voyage = voyage 
        template.contract = self.get_contract(response.contract)
        template.xml_response = response
        template.save()  
        self.delete_data(pk)        
        for xml_draft in response.drafts.draft:            
            draft = Draft()
            fields = ['name','guid','date','shipper','consignee','finalDestination','POD','POL','finstatus','status','poruchenie','poruchenieNums','notify']
            for field in fields:
                value = u'%s' % xml_draft[field] if xml_draft[field] else xml_draft[field]                        
                setattr(draft, field, value)                
            draft.user = User.objects.get(profile__guid=xml_draft.userguid)                                
            draft.voyage = self.get_voyage(xml_draft.voyage) 
            draft.line = self.get_line(xml_draft.line)
            draft.template = template               
            draft.save()
            fields = ['name','SOC','size','type','seal','cargo','netto','gross','tare','package','quantity']
            for xml_container in xml_draft.containers.container:
                container = Container()
                for field in fields:
                    value = u'%s' % xml_container[field] if xml_container[field] else xml_container[field]  
                    setattr(container, field, value)
                container.line = self.get_line(xml_container.line)
                container.draft = draft
                container.save()
            fields = ['size','type','ordered','done',]    
            for xml_readiness in xml_draft.readiness.row:
                readiness = Readiness()
                for field in fields:                    
                    setattr(readiness, field, xml_readiness[field])                
                readiness.draft = draft
                readiness.save()
        
            
    def delete_data(self, pk):
        template = UploadedTemplate.objects.get(pk=pk)
        drafts = Draft.objects.filter(template=template)
        drafts.delete()                        