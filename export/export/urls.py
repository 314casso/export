from django.conf.urls import patterns, include, url
from django.conf import settings
from nutep.views import services, landing, upload_file, TemplateDeleteView
from django.contrib.auth import views as auth_views


from django.contrib import admin
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
    url(r'^services/$', services, name='services'),
    url(r'^upload/$', upload_file, name='upload'),
    url(r'^deletetemplate/(?P<pk>[0-9]+)$', TemplateDeleteView.as_view(), name='delete-template'),  
)


if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns