from django.conf.urls import url
from .views import index, prueba, matriz_mid, matriz_1mao, matriz_2mao, matriz_3mao
from .views import Crear_estudio, Listar_actor, Crear_actor, Editar_actor, Eliminar_actor, Crear_ficha, \
    Crear_objetivo, Listar_objetivo, Editar_objetivo, Eliminar_objetivo, Crear_relacionInfluencia, Crear_1mao,\
    Crear_2mao
from .views import actor_ajax, consultar_ficha, consultar_desc_obj

# nombre de la url, view que respondera y el parametro name
urlpatterns = [
    url(r'^$', index, name=index),
    url(r'^prueba$', matriz_1mao, name='matriz_1mao'),

# Urls modelo Estudio_mactor
    url(r'^estudio$', Crear_estudio.as_view(), name='formEstudio'),

# Urls modelo Actor
    url(r'^actor$', Crear_actor.as_view(), name='formActor'),
    url(r'^lista_actores', Listar_actor.as_view(), name='listar_actor'),
    url(r'^editar_actor/(?P<pk>\d+)/$', Editar_actor.as_view(), name='editar_actor'),
    url(r'^eliminar_actor/(?P<pk>\d+)/$', Eliminar_actor.as_view(), name='eliminar_actor'),

# Urls modelo ficha_actor
    url(r'^ficha$', Crear_ficha.as_view(), name='ficha'),

# Urls modelo Objetivo
    url(r'^objetivo$', Crear_objetivo.as_view(), name='objetivo'),
    url(r'^lista_objetivos', Listar_objetivo.as_view(), name='listar_objetivo'),
    url(r'^editar_objetivo/(?P<pk>\d+)/$', Editar_objetivo.as_view(), name='editar_objetivo'),
    url(r'^eliminar_objetivo/(?P<pk>\d+)/$', Eliminar_objetivo.as_view(), name='eliminar_objetivo'),

# Urls modelo influencias y matrices
    url(r'^influencia$', Crear_relacionInfluencia.as_view(), name='influencia'),
    url(r'^matriz_mid$', matriz_mid, name='matriz_mid'),
    url(r'^1mao$', Crear_1mao.as_view(), name='1mao'),
    url(r'^matriz_1mao$', matriz_1mao, name='matriz_1mao'),
    url(r'^2mao$', Crear_2mao.as_view(), name='2mao'),
    url(r'^matriz_2mao$', matriz_2mao, name='matriz_2mao'),
    url(r'^matriz_3mao$', matriz_3mao, name='matriz_3mao'),

# Urls peticiones ajax
    url(r'^actor-ajax/$', actor_ajax),
    url(r'^actor-ajax2/$', consultar_ficha),
    url(r'^objetivo-ajax/$', consultar_desc_obj),





]