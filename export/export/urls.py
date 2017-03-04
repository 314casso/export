from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from nutep.views import landing, upload_file, TemplateDeleteView,\
get_template_status, ServiceView, TemplateDetailView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'export.views.home', name='home'),
    # url(r'^export/', include('export.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('', 
    url(r'^$', landing, name='landing'),
    url(r'^services/$', ServiceView.as_view(), name='services'),
    url(r'^upload/$', upload_file, name='upload'),
    url(r'^deletetemplate/(?P<pk>[0-9]+)$', TemplateDeleteView.as_view(), name='delete-template'),  
    url(r'^gettemplate/(?P<pk>[0-9]+)$', get_template_status, name='get-template'),
    url(r'^templatedetails/(?P<pk>[0-9]+)$', TemplateDetailView.as_view(), name='template-details'),
)


if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns