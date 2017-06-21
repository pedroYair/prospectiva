from django.conf.urls import url
from .views import index, prueba, matriz
from .views import Crear_estudio, Listar_actor, Crear_actor, Editar_actor, Eliminar_actor, \
    Crear_ficha, Listar_ficha, \
    Crear_objetivo, Listar_objetivo, Editar_objetivo, Eliminar_objetivo, Crear_relacionInfluencia

from .ajax import eliminar_actor

# nombre de la url, view que respondera y el parametro name
urlpatterns = [
    url(r'^$', index, name=index),
    url(r'^prueba$', prueba, name='prueba'),
# Urls modelo Estudio_mactor
    url(r'^estudio$', Crear_estudio.as_view(), name='formEstudio'),
# Urls modelo Actor
    url(r'^actor$', Crear_actor.as_view(), name='formActor'),
    url(r'^lista_actores', Listar_actor.as_view(), name='listar_actor'),
    url(r'^editar_actor/(?P<pk>\d+)/$', Editar_actor.as_view(), name='editar_actor'),
    url(r'^eliminar_actor/(?P<pk>\d+)/$', Eliminar_actor.as_view(), name='eliminar_actor'),

    url(r'^matriz', matriz, name='matriz'),
# Urls modelo Ficha
    url(r'^ficha$', Crear_ficha.as_view(), name='formFicha'),
    url(r'^lista_fichas', Listar_ficha.as_view(), name='listar_ficha'),
# Urls modelo Objetivo
    url(r'^objetivo$', Crear_objetivo.as_view(), name='objetivo'),
    url(r'^lista_objetivos', Listar_objetivo.as_view(), name='listar_objetivo'),
    url(r'^editar_objetivo/(?P<pk>\d+)/$', Editar_objetivo.as_view(), name='editar_objetivo'),
    url(r'^eliminar_objetivo/(?P<pk>\d+)/$', Eliminar_objetivo.as_view(), name='eliminar_objetivo'),
# Urls modelo Influencia
    url(r'^influencia$', Crear_relacionInfluencia.as_view(), name='influencia'),

]