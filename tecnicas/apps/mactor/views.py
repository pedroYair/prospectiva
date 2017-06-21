from django.http import request
from django.shortcuts import render, redirect
from .models import Estudio_Mactor, Actor, Ficha, Objetivo, Relacion_Influencia
from .forms import Formulario_Estudio, Formulario_actor, Formulario_Ficha, Formulario_objetivo, Formulario_Influencia
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User

# VIEW MODELO ESTUDIO MACTOR--------------------------------------------------------------------->

class Crear_estudio(CreateView):
    model = Estudio_Mactor
    form_class = Formulario_Estudio
    template_name = 'Estudio/create_estudio.html'
    success_url = reverse_lazy('mactor:formActor')

# VIEWS MODELO ACTOR------------------------------------------------------------------------------>

class Crear_actor(CreateView):
    model = Actor
    form_class = Formulario_actor
    template_name = 'actor/create_actor.html'
    success_url = reverse_lazy('mactor:listar_actor')

class Listar_actor(ListView):
    model = Actor
    template_name = 'actor/list_actor.html'
    paginate_by = 15
    ordering = ('nombreLargo',)

class Editar_actor(UpdateView):
    model = Actor
    form_class = Formulario_actor
    template_name = 'actor/matriz.html'
    success_url = reverse_lazy('mactor:editar_actor')

class Eliminar_actor(DeleteView):
    model = Actor
    template_name = 'actor/delete_actor.html'
    success_url = reverse_lazy('mactor:listar_actor')

# VIEWS MODELO FICHA----------------------------------------------------------------------------------------------------->

class Crear_ficha(CreateView):
    model = Ficha
    form_class = Formulario_Ficha
    template_name = 'ficha/create_ficha.html'
    success_url = reverse_lazy('mactor:listar_ficha')

class Listar_ficha(ListView):
    model = Ficha
    template_name = 'ficha/list_ficha.html'
    paginate_by = 5

# VIEWS FORMULARIO OBJETIVO--------------------------------------------------------------------------------------------->

class Crear_objetivo(CreateView):
    model = Objetivo
    form_class = Formulario_objetivo
    template_name = 'objetivo/create_objetivo.html'
    success_url = reverse_lazy('mactor:listar_objetivo')

class Listar_objetivo(ListView):
    model = Objetivo
    template_name = 'objetivo/list_objetivo.html'
    paginate_by = 15

class Editar_objetivo(UpdateView):
    model = Objetivo
    form_class = Formulario_objetivo
    template_name = 'objetivo/create_objetivo.html'
    success_url = reverse_lazy('mactor:listar_objetivo')

class Eliminar_objetivo(DeleteView):
    model = Objetivo
    template_name = 'objetivo/delete_objetivo.html'
    success_url = reverse_lazy('mactor:listar_objetivo')

# VIEWS INFLUENCIA------------------------------------------------------------------------------------------------>

class Crear_relacionInfluencia(CreateView):
    model = Relacion_Influencia
    form_class = Formulario_Influencia
    template_name = 'influencia/create_influencia.html'
    success_url = reverse_lazy('mactor:influencia')

#registro de la influencia de un actor sobre si mismo automaticamente = 0
    actor = Actor.objects.all().order_by('id')
    usu = User.objects.all().order_by('id')
    inf = Relacion_Influencia.objects.all().order_by('id')
    cont = 0

    for i in inf:
        if i.actorX == i.actorY:
            cont += 1
    if cont == 0:
            for j in range(len(actor)):
                a = Relacion_Influencia()
                a.actorX = actor[j]
                a.actorY = actor[j]
                a.valor = 0
                a.creador = usu[1]
                a.justificacion = ""
                a.codigo_Estudio = 1
                a.save()


# Clase auxiliar para la generacion de la matriz de inlfuencias MID
class Valor_actor:

    def __init__(self, posicion, valor):
        self.posicion = posicion
        self.valor = valor

# View generadora de la matriz MID
def matriz(request):

    actor = Actor.objects.all().order_by('id')
    inf = Relacion_Influencia.objects.all().order_by('actorY', 'actorX')
    valores = [] # contiene los valores que se muestran en la matriz
    cont = 0     # cuenta las influencias
    cont2 = 0    # determina la posicion donde va el nombre corto dentro de valores
    pos_list = 0 # determina el nombre corto que se ha de colocar en valores

    for i in range(len(inf)):
        cont += 1
        valores.append(Valor_actor(posicion=cont, valor=inf[i].valor))
        if cont == actor.count():
            # determina la posicion donde se va a colocar el nombre corto de la nueva fila
            cont2 = (actor.count()+1)*pos_list
            # inserta el nombre corto de la nueva fila
            valores.insert(cont2, Valor_actor(posicion=0, valor=actor[pos_list].nombreCorto))
            cont = 0
            cont2 = 0
            pos_list += 1

    # ---------------------------------------------------------------------------------------------------------------->
    # formula MIDI ij = MID ij + Sum(Minimo [(MID ik, MID ik])

    def calcular_midi():
        cont = 0
        cont2 = 0
        pos_list = 0
        # contiene las sublistas de valores minimos por cada actor Y
        lista_minimo = []
        # contiene lista_minimo concatenado
        lista_total = []
        # contiene los valores correspondientes a MIDI
        valores_midi = []

        for i in range(len(inf)):
            if inf[i].actorY == inf[i].actorX:
                # se agrega la sublista correspondiente al actorY a lista_minimo
                lista_minimo.append(calcular_minimo(pos=i))

        #concatenacion de lista_minimo para facilitar la suma con las influencias correspondientes (igual longitud)
        for i in lista_minimo:
            lista_total += i

        # se realiza la suma MID ij + Sum(Minimo [(MID ik, MID ik])
        for i in range(len(inf)):
            cont += 1
            valores_midi.append(Valor_actor(posicion=cont, valor=inf[i].valor + lista_total[i]))
            print "------------"
            print inf[i].valor
            print lista_total[i]
            print inf[i].valor + lista_total[i]
            print "------------"
            if cont == actor.count():
                # determina la posicion donde se va a colocar el nombre corto de la nueva fila
                cont2 = (actor.count() + 1) * pos_list
                # inserta el nombre corto de la nueva fila
                valores_midi.insert(cont2, Valor_actor(posicion=0, valor=actor[pos_list].nombreCorto))
                cont = 0
                cont2 = 0
                pos_list += 1

        return valores_midi


    def calcular_minimo(pos):
        cont3 = 0 # posicion en inf
        cont4 = 0 # posicion en lista ordenada izq
        derecho = []
        izquierdo = []
        lista_ordenada_izq = []
        comparacion = []
        lista_suma = []

        # valores del lado izquierdo del minimo
        for i in range(len(inf)):
            lista_suma.append(0)
            if inf[i].actorY != inf[pos].actorY:
                # los valores son ingresados a la lista izquierdo
                izquierdo.append(inf[i].valor)
                #print inf[i].valor

        cont4 = 1
        # se asigna una posicion a cada elemento de izquierdo para facilitar la comparacion con la lista derecho
        for i in range(len(izquierdo)):
            lista_ordenada_izq.append(Valor_actor(posicion=cont4, valor=izquierdo[i]))
            #print lista_ordenada_izq[i].valor
            if len(lista_ordenada_izq) == actor.count():
                cont4 += 1

        # valores del lado derecho del minimo (corregir drecho = izquierdo en la formula)
        for i in range(len(inf)):
            if inf[pos].actorY != inf[i].actorX and inf[i].actorY == inf[pos].actorY and len(derecho) < actor.count() - 1:
                derecho.append(Valor_actor(posicion=cont3+1, valor=inf[i].valor))
                #print inf[pos].actorY
                #print inf[i].valor
                cont3 += 1

        # utilizada para iterar en la lista de valores derechos dentro de la comparacion
        cont4 = 0
        # contiene el resultado de comparar valor derecho vs izquierdo (cual es menor)

        # se realiza la comparacion entre los elementos de derecho e izquierdo valor minimo
        for i in range(len(lista_ordenada_izq)):
            if derecho[cont4].posicion == lista_ordenada_izq[i].posicion and cont4 <= actor.count():
                if derecho[cont4].valor <= lista_ordenada_izq[i].valor:
                    comparacion.append(derecho[cont4].valor)
                else:
                    comparacion.append(lista_ordenada_izq[i].valor)
            else:
                cont4 += 1
                if derecho[cont4].posicion == lista_ordenada_izq[i].posicion:
                    if derecho[cont4].valor <= lista_ordenada_izq[i].valor:
                        comparacion.append(derecho[cont4].valor)
                    else:
                        comparacion.append(lista_ordenada_izq[i].valor)
        # indica el punto inicial de la sublista
        ini = 0
        # indica el punto final de la sublista
        fin = actor.count()
        # la lista comparacion es divida y sumada
        for i in range(fin):
            if i < actor.count() - 1:
                # se obtiene la suma de Min (formula MIDI)
                lista_suma = map(sum, zip(lista_suma, comparacion[ini:fin]))
                ini = fin
                fin = fin + actor.count()

        return lista_suma

    midi = calcular_midi()

    contexto = {'actores': actor, 'mitad': actor.count(), 'valores': valores, 'valores_midi': midi}
    return render(request, 'influencia/matriz.html', contexto)





def index(request):
    return render(request, 'index.html')


def prueba(request):
    return render(request, 'baseForms/base_forms.html')

