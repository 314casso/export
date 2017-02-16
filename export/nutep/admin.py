from django.contrib import admin
from nutep.models import UploadedTemplate


class UploadedTemplateAdmin(admin.ModelAdmin):
    list_display = ('attachment', 'history')
    def queryset(self, request):
        return UploadedTemplate.all_objects.all()

admin.site.register(UploadedTemplate, UploadedTemplateAdmin)
  

