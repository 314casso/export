# -*- coding: utf-8 -*-

from django.utils.encoding import force_unicode
from django.shortcuts import render
import logging
from django.contrib.auth.decorators import login_required
from nutep.models import UploadedTemplate
from django.http import HttpResponseRedirect, HttpResponse
from nutep.forms import TemplateForm
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
import json


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
def services(request):
    PER_PAGE = 10
    template_list = UploadedTemplate.objects.filter(history__user=request.user).distinct()    
    
    page = request.GET.get('page', 1)

    paginator = Paginator(template_list, PER_PAGE)
    try:
        templates = paginator.page(page)
    except PageNotAnInteger:
        templates = paginator.page(1)
    except EmptyPage:
        templates = paginator.page(paginator.num_pages)
    
    template_form = TemplateForm()    
    context = {
               'title' : force_unicode('Рускон Онлайн'),
               'templates' : templates,
               'template_form': template_form,
               'paginator': paginator,
               'page_obj': templates,
               'is_paginated': templates.has_other_pages(),
               'object_list': templates.object_list                                             
              }    
    return render(request, 'base.html', context)


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
        
    
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():            
            template = form.save(commit=False)
            template.user = request.user
            template.save()
            return HttpResponseRedirect(reverse(services))