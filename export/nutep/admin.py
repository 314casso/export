from django.contrib import admin
from nutep.models import UploadedTemplate, Voyage, UserProfile, Contract, Line,\
    Terminal, Vessel, Draft, Container, BaseError
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.unregister(User)


class UploadedTemplateAdmin(admin.ModelAdmin):
    list_display = ('attachment', 'history')
    def queryset(self, request):
        return UploadedTemplate.all_objects.all()


class VoyageAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ContractInline(admin.TabularInline):
    model = Contract
    extra = 0
    

class LineAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [ ContractInline, ]


class TerminalAdmin(admin.ModelAdmin):
    list_display = ('name', )


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
    
class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]


admin.site.register(User, UserProfileAdmin)
admin.site.register(UploadedTemplate, UploadedTemplateAdmin)
admin.site.register(Voyage, VoyageAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(Terminal, TerminalAdmin)
admin.site.register(Vessel)
admin.site.register(Draft)
admin.site.register(Container)
admin.site.register(BaseError)

