from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from mezzanine.core.fields import RichTextField
from .models import Tema, Experimento, Revision
from mezzanine.pages.page_processors import processor_for

# para ver la lista de RadioSelect dispuestos horizontalmente
# (estos son los botones de puntuacion de 1-5)
class VerHorizontal(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

# forma para crear nuevo tema
class TemaForm(forms.Form):
    title = forms.CharField(label="Título",max_length=40)

# forma para crear nuevo experimento
class ExperimentoForm(forms.Form):
    titulo = forms.CharField(label="Título",max_length=40)
    texto = RichTextField().formfield(max_length=60000)

# forma para crear nueva revision
class RevisionForm(forms.Form):
    attrs = {'rows':4,'required': True}
    coment = forms.CharField(widget=forms.Textarea(attrs),
            label="Comentario",max_length=1200)
    CHOICES = [(1,'1 '),(2,'2 '),(3,'3 '),(4,'4 '),(5,'5 ')]
    nota = forms.ChoiceField(choices=CHOICES, label='Calificación',
            widget=forms.RadioSelect(renderer=VerHorizontal))
    tiempo = forms.TimeField(label='Tiempo Utilizado (h:m)')

# forma para eliminar experimento
class DeleteExpeForm(forms.Form):
    accion = forms.CharField(label="",max_length=10)

# forma para borrar revision
class DeleteRevisionForm(forms.Form):
    CHOICES = [('no borra','No '),('borra','Sí')]
    orden = forms.ChoiceField(choices=CHOICES, label="",
            widget=forms.RadioSelect(renderer=VerHorizontal))

# calculo de la calificacion promedio para un experimento
def calificacion_promedio(revisiones):
    decimales = 1
    num_revisiones = len(revisiones)
    if num_revisiones == 0:
        return 0
    suma = 0
    for revision in revisiones:
        suma = suma + revision.rating
    return round(float(suma)/num_revisiones, decimales)

# determina si un usuario ya realizo una revision a un experimento
def experimento_revisado(user,revisiones):
    reviso = True
    if user.is_authenticated:
        reviso = revisiones.filter(author=user).exists()
    return reviso

# procesador de pagina de clase Experimento
# ver http://mezzanine.jupo.org/docs/content-architecture.html#page-processors
# para seguir tutorial paso a paso empesar en
# http://mezzanine.jupo.org/docs/content-architecture.html#the-page-model
@processor_for(Experimento)
def edit_expe_form(request, page):
    # inicializacion
    expe = page.experimento
    user = request.user
    revisiones = Revision.objects.filter(experimento=expe).order_by('-pub_date')
    nota_prom = calificacion_promedio(revisiones)
    data = {'titulo': page.title, 'texto': expe.texto}
    form_edit_expe = ExperimentoForm(initial=data)
    form_revision = RevisionForm()
    form_delete_expe = DeleteExpeForm()
    form_del_rev = DeleteRevisionForm()
    reviso_expe = experimento_revisado(user,revisiones)
    if request.method == "POST":
        form_edit_expe = ExperimentoForm(request.POST)
        form_revision = RevisionForm(request.POST)
        form_delete_expe = DeleteExpeForm(request.POST)
        form_del_rev = DeleteRevisionForm(request.POST)
        # cuando el usuario hace clic en un formulario se verifica
        # el siguiente bloque para ejecutar la acción correspondiente
        # a ese formulario en particular
        if "btEditExpe" in request.POST and form_edit_expe.is_valid():
            #print(page.experimento.autor.__dict__)
            titulo = form_edit_expe.data.get("titulo")
            texto = form_edit_expe.data.get("texto")
            Experimento.objects.filter(id=page.id).update(texto=texto)
            page.title = titulo
            page.save()
            redirect = request.path + "?submitted=true"
            return HttpResponseRedirect(redirect)
        elif form_revision.is_valid():
            coment = form_revision.data.get("coment")
            author = request.user
            expe = page.experimento
            nota = form_revision.data.get("nota")
            time = form_revision.data.get("tiempo")
            date = timezone.now()
            if "btEditRev" in request.POST:
                author = User.objects.get(username=request.POST.get("btEditRev"))
                rev = revisiones.filter(author=author)
                rev.update(mod_date=date, body_text=coment, rating=nota, tiempo=time)
            elif "btcreateRev" in request.POST:
                newR = Revision(experimento=expe, author=author, pub_date=date,
                    mod_date=date, body_text=coment, rating=nota, tiempo=time)
                newR.save()
            redirect = request.path + "?submitted=true"
            return HttpResponseRedirect(redirect)
        elif "btBorrarExp" in request.POST and form_delete_expe.is_valid():
            accion = form_delete_expe.data.get("accion")
            if accion == "borrar":
                parentPage = page.parent
                redirect = parentPage.get_absolute_url()
                revisiones.delete()
                Experimento.objects.filter(id=page.id).delete()
            else:
                redirect = request.path
            return HttpResponseRedirect(redirect)
        elif "btBorrarRev" in request.POST and form_del_rev.is_valid():
            orden = form_del_rev.data.get("orden")
            if orden == "borra":
                author = User.objects.get(username=request.POST.get("btBorrarRev"))
                revisiones.filter(author=author).delete()
            redirect = request.path + "?submitted=true"
            return HttpResponseRedirect(redirect)
    return {'form_edit_expe':form_edit_expe,'form_delete_expe':form_delete_expe,
        'revisiones':revisiones,'reviso_expe':reviso_expe,'form_del_rev':form_del_rev,
        'form_revision':form_revision,'nota_prom':nota_prom}

# procesador de pagina de clase Tema
@processor_for(Tema)
def tema_form(request, page):
    temaForm = TemaForm()
    expeForm = ExperimentoForm()
    if request.method == "POST":
        temaForm = TemaForm(request.POST)
        expeForm = ExperimentoForm(request.POST)
        # ya que Tema posee dos formularios, en este bloque se define
        # la accion adecuada para cada uno
        if "btCrearTema" in request.POST and temaForm.is_valid():
            title = temaForm.data.get("title")
            fecha = timezone.now()
            newpage = Tema.objects.create(title=title, dob=fecha)
            newpage.set_parent(page)
            page.save()
            redirect = request.path + "?submitted=true"
            return HttpResponseRedirect(redirect)
        elif "btCrearExpe" in request.POST and expeForm.is_valid():
            title = expeForm.data.get("titulo")
            autor = request.user
            texto = expeForm.data.get("texto")
            query = Experimento.objects
            newpage = query.create(title=title,autor=autor,texto=texto)
            newpage.set_parent(page)
            page.save()
            #redirect = request.path + "?submitted=true"
            redirect = newpage.get_absolute_url()
            return HttpResponseRedirect(redirect)
    return {"temaForm": temaForm, "expeForm":expeForm}
