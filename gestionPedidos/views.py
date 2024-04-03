from django.shortcuts import render
from django.http import HttpResponse
from gestionPedidos.models import Articulos
from django.core.mail import send_mail
from django.conf import settings
from gestionPedidos.forms import FormularioContacto
# Create your views here.

def busqueda_productos(request):
    return render(request, "busqueda_productos.html")

def buscar(request):
    if request.GET["prd"]:
        #mensaje="Articulo buscado: %r" %request.GET["prd"]
        producto=request.GET["prd"]
        if len(producto)>20:
            mensaje="Texto de busqueda muy largo"
        else:

            articulos=Articulos.objects.filter(nombre__icontains=producto)
        
            return render(request, "resultados_busqueda.html",{"articulos":articulos, "query":producto})
    else:
        mensaje= "No has ingresado nada"

    return HttpResponse(mensaje)
"""
def contacto(request):
    if request.method=="POST":

        subject=request.POST["asunto"]
        message=request.POST["mensaje"]+ " "+ request.POST["email"]
        email_from=settings.EMAIL_HOST_USER
        recipient_list=["diegolds221@gmail.com"]
        send_mail(subject,message,email_from,recipient_list, fail_silently=False)

        return render(request, "gracias.html")
    return render(request, "contacto.html")
"""
def contacto(request):
    if request.method=="POST":

        miFormulario=FormularioContacto(request.POST)
        if miFormulario.is_valid():
            infForm=miFormulario.cleaned_data

            send_mail(infForm['asunto'], infForm['mensaje'], infForm.get('email',''),['diegolds221@gmail.com'],)

            return render(request, "gracias.html")
    else:
        miFormulario=FormularioContacto()
    
    return render(request, "formulario_contacto.html",{"form":miFormulario})