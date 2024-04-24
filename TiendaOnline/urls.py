"""
URL configuration for TiendaOnline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestionPedidos import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('busqueda_productos/', views.busqueda_productos),
    path('buscar/', views.buscar),
    path('contacto/', views.contacto),
    path('tabla_personas/', views.tabla_personas, name='tabla_personas'),
    path('tabla_implementos/', views.tabla_reservas, name='tabla_reservas'),
    #path('buscar-implemento/', views.buscar_implemento, name='buscar_implemento'),
    #path('filtrar-por-edificio/', views.filtrar_por_edificio, name='filtrar_por_edificio'),
    path('buscar_y_filtrar_implemento/', views.buscar_y_filtrar_implemento, name='buscar_y_filtrar_implemento'),
]
