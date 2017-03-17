# -*- coding: utf-8 -*-

from django.utils.encoding import force_unicode
from django.shortcuts import render
import logging
from django.contrib.auth.decorators import login_required
from nutep.models import UploadedTemplate, Voyage, Vessel,\
    Draft
from django.http import HttpResponseRedirect, HttpResponse
from nutep.forms import TemplateForm
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
import json
from django.core.files.base import ContentFile
from nutep.services import DraftService
from export.local_settings import WEB_SERVISES
from django.views.generic.base import TemplateView
from django.views.decorators.http import require_http_methods


logger = logging.getLogger('django.request')


class DeleteMixin(SingleObjectMixin):
    @method_decorator(login_required)   
    def dispatch(self, *args, **kwargs):
        return super(DeleteMixin, self).dispatch(*args, **kwargs)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.user = self.request.user
        self.object.deleted = True
        self.object.save()        
        return HttpResponse(json.dumps({'pk':self.object.id}), content_type="application/json") 
        
        
class TemplateDeleteView(DeleteMixin, DeleteView):   
    model = UploadedTemplate


@login_required
def template_detail(request, pk):
    template = UploadedTemplate.objects.get(pk=pk)    
    context = {
                'template_detail.html': template,
              }    
    return render(request, 'base.html', context)


class BaseView(TemplateView):    
    @method_decorator(login_required)   
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)        
        vessels = Vessel.objects.filter(history__user=self.request.user).distinct()       
        context.update({
                   'title' : force_unicode('Рускон Онлайн'),        
                   'vessels': vessels,                                             
                  })     
        return context
    

class ServiceView(BaseView):
    template_name = 'base.html'
    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        PER_PAGE = 10
        template_list = UploadedTemplate.objects.filter(history__user=self.request.user).distinct()    
        
        page = self.request.GET.get('page', 1)
    
        paginator = Paginator(template_list, PER_PAGE)
        try:
            templates = paginator.page(page)
        except PageNotAnInteger:
            templates = paginator.page(1)
        except EmptyPage:
            templates = paginator.page(paginator.num_pages)
        
        template_form = TemplateForm()    
        context.update({
                   'title' : force_unicode('Рускон Онлайн'),
                   'templates' : templates,
                   'template_form': template_form,
                   'paginator': paginator,
                   'page_obj': templates,
                   'is_paginated': templates.has_other_pages(),
                   'object_list': templates.object_list,
                  })     
        return context   


class TemplateDetailView(BaseView):
    template_name = 'template_details.html'
    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')        
        template = UploadedTemplate.objects.get(pk=pk)
        context = super(TemplateDetailView, self).get_context_data(**kwargs)
        context.update({
                   'title' : force_unicode('Рускон Онлайн'),
                   'template' : template,
                  })
        return context


class DraftDetailView(BaseView):
    template_name = 'draft_details.html'
    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        draft = Draft.objects.get(pk=pk)
        context = super(DraftDetailView, self).get_context_data(**kwargs)
        context.update({
                   'title' : force_unicode('Рускон Онлайн'),
                   'draft' : draft,
                  })
        return context


def landing(request):
    context = {
               'title' : force_unicode('Рускон'),                                             
              }     
    return render(request, 'landing.html', context)


@login_required
def delete_template(request, template_id):
    if request.method == 'POST':
        try:
            template = UploadedTemplate.objects.get(pk=template_id)
            template.deleted = True
            template.user = request.user
            template.save()            
        except UploadedTemplate.DoesNotExist:
            return HttpResponse(u'Template id %s не найден' % template_id, status=404)


@require_http_methods(["POST"])
@login_required    
def get_template_status(request, pk):
    if request.method == 'POST':
        draft_service = DraftService(WEB_SERVISES['draft'])    
        response = draft_service.update_status(pk)
        status = True if response else False                
        return HttpResponse(json.dumps({'status':status}), content_type="application/json")
            

@require_http_methods(["POST"])    
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():     
            filename = form.cleaned_data['attachment']
                        
            from openpyxl import load_workbook
            
            try:                         
                wb = load_workbook(filename = ContentFile(filename.read()))
            except Exception as e:
                return HttpResponse(u'Неверный формат шаблона: %s' % e.message,  status=400)
                
            ws = wb.active
            
            voyage_col_name = 'VOYAGE'
            voyage_cell = None 
            for row in ws.iter_rows(min_row=1, max_col=ws.max_column, max_row=ws.max_row):                
                if voyage_cell:
                    break
                for cell in row:
                    if cell.value and cell.value.upper() == voyage_col_name:
                        voyage_cell = cell
                        break                                  
            
            if not voyage_cell:
                return HttpResponse(u'Неверный шаблон. Столбец Voyage не найден в файле', status=400)
            
            rng = "%s%s:%s%s" % (voyage_cell.column, int(voyage_cell.row)+1,voyage_cell.column, int(voyage_cell.row)+1)
            voyages = set() 
            for row in ws.iter_rows(rng):
                voyages.add(row[0].value)
        
            voyage_name = None
            if len(voyages) == 1:
                voyage_name = voyages.pop()
            elif len(voyages) == 0:                
                return HttpResponse(u'Неверный шаблон. Столбец Voyage не заполнен', status=400)
            else:
                return HttpResponse(u'Неверный шаблон. Столбец Voyage содержит более одного рейса %s' % u','.join(voyages), status=400)
            
            voyage = None
            
            q = Voyage.objects.filter(name=voyage_name, history__user=request.user)[:1]
            if q:
                voyage = q.get()
            else:   
                voyage = Voyage()
                voyage.name = voyage_name
                voyage.user = request.user
                voyage.save()            
            try:
                form.instance = UploadedTemplate.objects.get(voyage=voyage)
            except UploadedTemplate.DoesNotExist:
                pass
            
            
            template = form.save(commit=False)            
            template.user = request.user
            template.voyage = voyage
            template.attachment = form.cleaned_data['attachment']            
            template.save()
            
            
            draft_service = DraftService(WEB_SERVISES['draft'])    
            draft_service.load_draft(template, request.user)
                        
            return HttpResponseRedirect(reverse('services'))