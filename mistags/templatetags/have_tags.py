from django import forms
from django import template
from miapp.page_processors import RevisionForm

#from miapp.models import Tema
#from django.utils import timezone

register = template.Library()

@register.filter(name="have")
def have(pages,model_name):
    for page in pages:
        if page.in_menu and page.content_model == model_name:
            return True
    return False

@register.filter(name="rellenarRevisionForm")
def rellenar(rev,user):
    datos_rev = {'coment':rev.body_text,'nota':rev.rating,'tiempo':rev.tiempo}
    form = RevisionForm(initial=datos_rev)
    if rev.author != user:
        form.fields['nota'].widget = forms.HiddenInput()
        form.fields['tiempo'].widget = forms.HiddenInput()
    return form
