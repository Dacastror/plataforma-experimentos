from django.db import models
from mezzanine.pages.models import Page
from django.contrib.auth.models import User
from mezzanine.core.fields import RichTextField

class Tema(Page):
    dob = models.DateField("Date")

class Experimento(Page):
    autor = models.ForeignKey('auth.User', null=True)
    texto = RichTextField(null=True)

class Revision(models.Model):
    experimento = models.ForeignKey("Experimento")
    author = models.ForeignKey('auth.User', null=True)
    pub_date = models.DateTimeField()
    mod_date = models.DateTimeField()
    body_text = models.TextField()
    rating = models.IntegerField()
    tiempo = models.TimeField(null=True)
