from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

def template1(self):
    #Html = open("C:\Users\ALEJANDRO\Desktop\tercera_entrega\Django\Django\Templates\Template.html")
    #template = Template(Html.read())
    #Html.close()
    #Contexto = Context()
    #documento = template.render(Contexto)
    #....CODE IMPROVEMENT....#
    template= loader.get_template("template.html")
    documento=template.render()
    return HttpResponse(documento)