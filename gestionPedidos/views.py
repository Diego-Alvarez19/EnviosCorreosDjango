from django.shortcuts import render
from django.http import HttpResponse
from gestionPedidos.models import Articulos
from django.core.mail import send_mail
from django.conf import settings
from gestionPedidos.forms import FormularioContacto
from .models import Persona
from .models import Implemento_1
from django.template.loader import render_to_string
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone
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

# def tabla_reservas(request):
#     # Obtener todos los objetos del modelo
#     implementos = Implemento_1.objects.all()

#     # Aplicar filtros según los parámetros de la URL
#     implemento = request.GET.get('implemento')
#     edificio = request.GET.get('edificio')

#     if implemento:
#         implementos = implementos.filter(implemento=implemento)
#     if edificio:
#         implementos = implementos.filter(edificio=edificio)

#     # Renderizar la plantilla con los resultados filtrados
#     return render(request, 'disponibilidad.html', {'implementos': implementos})

# def buscar_y_filtrar_implemento(request):
#     # Obtener todos los objetos del modelo
#     implementos = Implemento_1.objects.all()

#     # Aplicar filtros según los parámetros de la URL
#     implemento = request.GET.get('implemento')
#     edificio = request.GET.get('edificio')

#     if implemento:
#         implementos = implementos.filter(implemento=implemento)
#     if edificio:
#         implementos = implementos.filter(edificio=edificio)

#     # Renderizar solo la tabla con los resultados filtrados
#     tabla_html = render_to_string('tabla_implementos_partial.html', {'implementos': implementos})

#     # Devolver la tabla HTML como respuesta AJAX
#     return JsonResponse({'tabla_html': tabla_html})

def tabla_reservas(request):
    print("Entrando a la función tabla reservas")
    # Obtener todos los objetos del modelo
    implementos = Implemento_1.objects.all()

   # Obtener la hora actual en UTC
    hora_actual_utc = timezone.now()
    print("Hora actual (UTC):", hora_actual_utc)

    # Ajustar la hora actual a la zona horaria de Bogotá (UTC-5)
    diferencia_horaria = timedelta(hours=-5)
    hora_actual_bogota = hora_actual_utc + diferencia_horaria
    print("Hora actual (Bogotá):", hora_actual_bogota.time())

    # Verificar y actualizar los implementos en reserva
    for implemento in implementos:
        if implemento.disponibilidad == 'En Reserva' and \
                implemento.reserva_confirmada is False and \
                implemento.hora_max_reserva_devolucion is not None:
            # Comparar con la hora máxima de reserva (hora local de Bogotá)
            if hora_actual_bogota.time() > implemento.hora_max_reserva_devolucion:
                print("La hora actual es mayor que la hora máxima de reserva.")
                implemento.disponibilidad = 'Disponible'
                implemento.hora_reserva = None
                implemento.hora_max_reserva_devolucion = None
                implemento.save()

    # Aplicar filtros según los parámetros de la URL
    implemento_param = request.GET.get('implemento')
    edificio_param = request.GET.get('edificio')

    if implemento_param:
        implementos = implementos.filter(implemento=implemento_param)
    if edificio_param:
        implementos = implementos.filter(edificio=edificio_param)

    # Renderizar la plantilla con los resultados filtrados
    return render(request, 'disponibilidad.html', {'implementos': implementos})

def buscar_y_filtrar_implemento(request):
    print("Entrando a la función buscar_y_filtrar_implemento")
    # Obtener todos los objetos del modelo
    implementos = Implemento_1.objects.all()

    # Obtener la hora actual en UTC
    hora_actual_utc = timezone.now()
    print("Hora actual (UTC):", hora_actual_utc)

    # Ajustar la hora actual a la zona horaria de Bogotá (UTC-5)
    diferencia_horaria = timedelta(hours=-5)
    hora_actual_bogota = hora_actual_utc + diferencia_horaria
    print("Hora actual (Bogotá):", hora_actual_bogota.time())

    # Verificar y actualizar los implementos en reserva
    for implemento in implementos:
        if implemento.disponibilidad == 'En Reserva' and \
                implemento.reserva_confirmada is False and \
                implemento.hora_max_reserva_devolucion is not None:
            print("Implemento:", implemento)
            print("Hora máxima de reserva:", implemento.hora_max_reserva_devolucion)

            # Comparar con la hora máxima de reserva (hora local de Bogotá)
            if hora_actual_bogota.time() > implemento.hora_max_reserva_devolucion:
                print("La hora actual es mayor que la hora máxima de reserva.")
                implemento.disponibilidad = 'Disponible'
                implemento.hora_reserva = None
                implemento.hora_max_reserva_devolucion = None
                implemento.save()

    # Aplicar filtros según los parámetros de la URL
    implemento_param = request.GET.get('implemento')
    edificio_param = request.GET.get('edificio')

    if implemento_param:
        implementos = implementos.filter(implemento=implemento_param)
    if edificio_param:
        implementos = implementos.filter(edificio=edificio_param)

    # Renderizar solo la tabla con los resultados filtrados
    tabla_html = render_to_string('tabla_implementos_partial.html', {'implementos': implementos})

    # Devolver la tabla HTML como respuesta AJAX
    return JsonResponse({'tabla_html': tabla_html})