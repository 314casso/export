# -*- coding: utf-8 -*-
from suds.client import Client
from __builtin__ import setattr
import base64
from suds.cache import NoCache
from nutep.models import Draft, UploadedTemplate, Voyage, Line, Vessel,\
    Contract
from django.contrib.auth.models import User


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
                        
    def update_status(self, pk):
        response = self._client.service.GetStatus(pk)      
        voyage = self.get_voyage(response.voyage)
        template = UploadedTemplate.objects.get(pk=pk)
        template.voyage = voyage 
        template.contract = self.get_contract(response.contract)
        template.xml_response = response
        template.save()  
        self.delete_data(pk)        
        for xml_draft in response.drafts.draft:
            print xml_draft
            draft = Draft()
            fields = ['name','guid','date','shipper','consignee','finalDestination','POD','POL','finstatus','status','poruchenie','poruchenieNums','notify']
            for field in fields:                        
                setattr(draft, field, xml_draft[field])                
                draft.user = User.objects.get(profile__guid=xml_draft.userguid)                                
                draft.voyage = self.get_voyage(xml_draft.voyage) 
                draft.line = self.get_line(xml_draft.line)
                draft.template = template               
            draft.save()
        return response
    
    def delete_data(self, pk):
        template = UploadedTemplate.objects.get(pk=pk)
        drafts = Draft.objects.filter(template=template)
        drafts.delete()
                    
    
    