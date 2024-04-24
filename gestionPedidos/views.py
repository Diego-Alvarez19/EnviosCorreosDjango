from django.shortcuts import render
from django.http import HttpResponse
from gestionPedidos.models import Articulos
from django.core.mail import send_mail
from django.conf import settings
from gestionPedidos.forms import FormularioContacto
from .models import Persona
from .models import Implemento
from django.template.loader import render_to_string
from django.http import JsonResponse

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

def tabla_personas(request):
    personas = Persona.objects.all()
    return render(request, 'tabla.html', {'personas': personas})

def tabla_reservas(request):
    # Obtener todos los objetos del modelo
    implementos = Implemento.objects.all()

    # Aplicar filtros según los parámetros de la URL
    nombre = request.GET.get('nombre')
    edificio = request.GET.get('edificio')

    if nombre:
        implementos = implementos.filter(nombre__icontains=nombre)
    if edificio:
        implementos = implementos.filter(edificio=edificio)

    # Renderizar la plantilla con los resultados filtrados
    return render(request, 'disponibilidad.html', {'implementos': implementos})

# def buscar_implemento(request):
#     # Lógica para buscar implementos por nombre
#     # Ejemplo:
#     nombre = request.GET.get('nombre')
#     implementos = Implemento.objects.filter(nombre__icontains=nombre)
#     return render(request, 'gestionPedidos/disponibilidad.html', {'implementos': implementos})

# def filtrar_por_edificio(request):
#     # Lógica para filtrar implementos por edificio
#     # Ejemplo:
#     edificio = request.GET.get('edificio')
#     implementos = Implemento.objects.filter(edificio=edificio)
#     return render(request, 'gestionPedidos/disponibilidad.html', {'implementos': implementos})

def buscar_y_filtrar_implemento(request):
    # Obtener todos los objetos del modelo
    implementos = Implemento.objects.all()

    # Aplicar filtros según los parámetros de la URL
    nombre = request.GET.get('nombre')
    edificio = request.GET.get('edificio')

    if nombre:
        implementos = implementos.filter(nombre__icontains=nombre)
    if edificio:
        implementos = implementos.filter(edificio=edificio)

    # Renderizar solo la tabla con los resultados filtrados
    tabla_html = render_to_string('tabla_implementos_partial.html', {'implementos': implementos})

    # Devolver la tabla HTML como respuesta AJAX
    return JsonResponse({'tabla_html': tabla_html})