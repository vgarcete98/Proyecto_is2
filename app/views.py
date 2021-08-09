from django.shortcuts import render
from django.template import loader, Context, Template
from django.http import HttpResponse



# Create your views here.

def home(request):
    doc_home=open("C:/ProyectoIS2/poliproyecto/app/templates/app/home.html")
    plt=Template(doc_home.read())
    doc_home.close()
    ctx=Context()
    documento=plt.render(ctx)
    return HttpResponse(documento)