from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from nutep.models import (BaseError, Container, Contract, Draft, Line,
                          Terminal, UploadedTemplate, UserProfile, Vessel,
                          Voyage)

admin.site.unregister(User)


class UploadedTemplateAdmin(admin.ModelAdmin):
    list_display = ('attachment', 'history')

    def queryset(self, request):
        return UploadedTemplate.all_objects.all()  # pylint: disable=E1101


class VoyageAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ContractInline(admin.TabularInline):
    model = Contract
    extra = 0


class LineAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [ContractInline, ]


class TerminalAdmin(admin.ModelAdmin):
    list_display = ('name', )


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]


admin.site.register(User, UserProfileAdmin)
admin.site.register(UploadedTemplate)
admin.site.register(Voyage, VoyageAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(Terminal, TerminalAdmin)
admin.site.register(Vessel)
admin.site.register(Draft)
admin.site.register(Container)
admin.site.register(BaseError)
