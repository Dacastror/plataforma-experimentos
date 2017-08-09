from copy import deepcopy
from django.contrib import admin
from .models import Tema , Experimento
from mezzanine.pages.admin import PageAdmin

# registro en el administrador de mezzanine
experimento_extra_fieldsets = ((None, {"fields": ("texto",)}),)

class TemaAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets)

class ExperimentoAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets) + experimento_extra_fieldsets

admin.site.register(Tema, TemaAdmin)
admin.site.register(Experimento, ExperimentoAdmin)
