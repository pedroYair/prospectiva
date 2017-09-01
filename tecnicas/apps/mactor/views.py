from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, request
from .models import Estudio_Mactor, Actor, Ficha_actor, Objetivo, Relacion_Influencia, Relacion_MAO
from .forms import Formulario_Estudio, Formulario_actor, Formulario_Ficha, Formulario_objetivo, Formulario_Influencia, \
    Formulario_1mao, Formulario_2mao
from django.views.generic import ListView, CreateView, UpdateView, DeleteView



# VIEW MODELO ESTUDIO MACTOR------------------------------------------------------------------------------------>

class Crear_estudio(CreateView):
    model = Estudio_Mactor
    form_class = Formulario_Estudio
    template_name = 'Estudio/create_estudio.html'
    success_url = reverse_lazy('mactor:formActor')


# VIEWS MODELO ACTOR-------------------------------------------------------------------------------------------->

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
    template_name = 'actor/create_actor.html'
    success_url = reverse_lazy('mactor:listar_actor')


class Eliminar_actor(DeleteView):
    model = Actor
    template_name = 'actor/delete_actor.html'
    success_url = reverse_lazy('mactor:listar_actor')

# VIEWS MODELO FICHA ACTOR-------------------------------------------------------------------------------------------->

class Crear_ficha(CreateView):
    model = Ficha_actor
    form_class = Formulario_Ficha
    template_name = 'Ficha/create_ficha_actor.html'
    success_url = reverse_lazy('mactor:ficha')


# VIEWS FORMULARIO OBJETIVO------------------------------------------------------------------------------------->

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


# VIEWS INFLUENCIAS DIRECTAS E INDIRECTAS----------------------------------------------------------------------->

# Ingresa las influencias con valor 0 de un actor sobre si mismo
def auto_influencia():  # debe recibir posteriormente el codigo del estudio, usuario
    # registro de la influencia de un actor sobre si mismo automaticamente = 0
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

class Crear_relacionInfluencia(CreateView):
    model = Relacion_Influencia
    form_class = Formulario_Influencia
    template_name = 'influencia/create_influencia.html'
    success_url = reverse_lazy('mactor:influencia')
    auto_influencia()


# View generadora de la matriz MID
def matriz_mid(request):

    actor = Actor.objects.all().order_by('id')
    inf = Relacion_Influencia.objects.all().order_by('actorY', 'actorX')
    valores = []    # contiene los valores que se muestran en la matriz
    cont = 0        # cuenta las influencias
    pos_list = 0    # determina el nombre corto que se ha de colocar en valores
    influencia = 0
    dependencia = 0

    for i in range(len(inf)):
        cont += 1
        valores.append(Valor_posicion(posicion=cont, valor=inf[i].valor))
        influencia += inf[i].valor  # se suman los valores de influencia directa
        if cont == actor.count():
            # se agrega el valor de la sumatoria de influencia directa del actor correspondiente
            valores.append(Valor_posicion(posicion=cont + 1, valor=influencia))
            # determina la posicion donde se va a colocar el nombre corto de la nueva fila
            cont2 = (actor.count() + 2) * pos_list
            # inserta el nombre corto de la nueva fila
            valores.insert(cont2, Valor_posicion(posicion=0, valor=actor[pos_list].nombreCorto))
            cont = 0
            pos_list += 1
            influencia = 0  # reinicio del valor de influencia

    # Agregado de la sumatoria de dependencias directas
    valores.append(Valor_posicion(posicion=0, valor="Dep. D"))
    cont = 1
    while cont <= actor.count():
        for i in valores:
            if i.posicion == cont:
                dependencia += i.valor
        valores.append(Valor_posicion(posicion=cont, valor=dependencia))
        cont += 1           # iteracion de las posiciones
        dependencia = 0     # reinicio a o del valor movilizacion

    midi = calcular_midi()  # obtencion de la matriz midi

    contexto = {'actores': actor, 'cantidad_mid': actor.count() + 1, 'cantidad_midi': actor.count() + 1,
                'valores': valores, 'valores_midi': midi}
    return render(request, 'influencia/matriz.html', contexto)

# VIEWS MATRIZ 1MAO---------------------------------------------------------------------------------------------------->

class Crear_1mao(CreateView):
    model = Relacion_MAO
    form_class = Formulario_1mao
    template_name = 'mao/create_1mao.html'
    success_url = reverse_lazy('mactor:1mao')

# View generadora de la matriz 1mao
def matriz_1mao(request):

    lista = generar_matriz_mao(2)                       # lista que contiene los parametros del contexto
    objetivo = Objetivo.objects.all().order_by('id')    # objetivos registrados
    actor = Actor.objects.all().order_by('id')          # actores registrados

    # objetivos:   lista de objetivos
    # actores:     lista de actores
    # valores:     valores de la matriz 2mao
    # cantidad:    cantidad de columnas, ayuda a establecer cuando hacer el salto de fila
    # cantidad2:   cantidad de columnas para las sumatorias de movilizacion (ultimas 3 filas)
    # valores_caa: valores de la matriz de convergencias
    # valores_daa: valores de la matriz de divergencias

    contexto = {'objetivos': lista[0], 'actores': lista[1], 'valores': lista[2], 'cantidad': objetivo.count() + 3,
                'cantidad2': lista[3], 'valores_caa': lista[4], 'cantidad3': actor.count(),
                'valores_daa': lista[5]}
    return render(request, 'mao/matriz_1mao.html', contexto)


# VIEWS MATRIZ 2MAO---------------------------------------------------------------------------------------------------->

class Crear_2mao(CreateView):
    model = Relacion_MAO
    form_class = Formulario_2mao
    template_name = 'mao/create_2mao.html'
    success_url = reverse_lazy('mactor:2mao')


# View generadora de la matriz 2mao
def matriz_2mao(request):

    lista = generar_matriz_mao(1)
    objetivo = Objetivo.objects.all().order_by('id')  # objetivos registrados
    actor = Actor.objects.all().order_by('id')  # actores registrados

    contexto = {'objetivos': lista[0], 'actores': lista[1], 'valores': lista[2], 'cantidad': objetivo.count() + 3,
                'cantidad2': lista[3], 'valores_caa': lista[4], 'cantidad3': actor.count(),
                'valores_daa': lista[5]}
    return render(request, 'mao/matriz_2mao.html', contexto)


# -------------------------------------CLASES AUXILIARES--------------------------------------------------------------->

# Clase auxiliar para la generacion de matrices, se asigna una posicion a un respectivo valor
class Valor_posicion:
    def __init__(self, posicion, valor):
        self.posicion = posicion
        self.valor = valor


# -------------------------------------FUNCIONES AUXILIARES------------------------------------------------------------>

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Funciones influencias entre actores>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Geracion de la matriz MIDIij = MID ij + Sum(Minimo [(MID ik, MID ik])
def calcular_midi():
    actor = Actor.objects.all().order_by('id')
    inf = Relacion_Influencia.objects.all().order_by('actorY', 'actorX')
    lista_minimo = []     # contiene las sublistas de valores minimos por cada actor Y
    lista_total = []      # contiene lista_minimo concatenado
    valores_midi = []     # contiene los valores correspondientes a MIDI

    # se agrega la sublista de valores minimos correspondiente al actorY a lista_minimo
    for i in range(len(inf)):
        if inf[i].actorY == inf[i].actorX:
            lista_minimo.append(calcular_minimo(pos=i))  # cada valor de pos permite el calculo de una fila de la matriz

    # concatenacion de lista_minimo para facilitar la suma con las influencias correspondientes (igual longitud)
    for i in lista_minimo:
        lista_total += i

    cont = 0
    pos_list = 0
    li = 0
    # se realiza la suma MID ij + Sum(Minimo [(MID ik, MID ik])
    for i in range(len(inf)):
        cont += 1
        valores_midi.append(Valor_posicion(posicion=cont, valor=inf[i].valor + lista_total[i]))
        # calcula el valor li
        if inf[i].actorY != inf[i].actorX and cont <= actor.count():
            li += inf[i].valor + lista_total[i]
        # determina la posicion donde se va a colocar el nombre corto de la nueva fila
        if cont == actor.count():
            cont2 = (actor.count() + 2) * pos_list
            # inserta el nombre corto de la nueva fila
            valores_midi.insert(cont2, Valor_posicion(posicion=0, valor=actor[pos_list].nombreCorto))
            # calcula los valor li (ultima columna)
            cont3 = cont2 + actor.count() + 1
            # inserta el valor li en la lista de valores midi de acuerdo a la posicion establecida
            valores_midi.insert(cont3, Valor_posicion(posicion=actor.count() + 1, valor=li))
            cont = 0
            pos_list += 1
            li = 0

    # calcula los valores di (ultima fila)
    valores_midi.append(Valor_posicion(posicion=0, valor="Di"))
    cont = 1
    di = 0
    suma_di = 0
    while cont <= actor.count():
        for i in valores_midi:
            if i.posicion == cont:
                di += i.valor
        cont2 = valores_midi[((actor.count() + 2) * (cont - 1)) + cont].valor
        di = di - cont2  # resta de la influencia indirecta que tiene un actor sobre si mismo
        valores_midi.append(Valor_posicion(posicion="", valor=di))  # sumatoria di de cada columna
        suma_di += di  # sumatoria de los valores di
        cont += 1      # iteracion de las posiciones
        di = 0         # reinicio a o del valor di
    valores_midi.append(Valor_posicion(posicion="", valor=suma_di))  # sumatoria total

    return valores_midi


# Realiza la parte derecha de la formula: Sum(Minimo [(MID ik, MID ik])
def calcular_minimo(pos):
    actor = Actor.objects.all().order_by('id')
    inf = Relacion_Influencia.objects.all().order_by('actorY', 'actorX')
    izquierdo = []  # contiene los valores izquierdos a comparar
    derecho = []  # contiene los valores derechos a comparar
    comparacion = []  # contiene los valores minimos establecidos al comparar izquierdo vs derecho
    lista_suma = []  # contiene la suma de los valores minimos establecidos al comparar

    # valores del lado derecho del minimo: influencias de los actores influenciados por Y sobre X excepto Y
    cont = 1
    aux = 0
    for i in range(len(inf)):
        lista_suma.append(0)
        if inf[i].actorY != inf[pos].actorY:
            derecho.append(Valor_posicion(posicion=cont, valor=inf[i].valor))
            aux += 1
            if aux == actor.count():
                cont += 1
                aux = 0

    cont = 0
    # valores del lado izquierdo del minimo: influencias del actor Y sobre los demas
    for i in range(len(inf)):
        if inf[pos].actorY != inf[i].actorX and inf[i].actorY == inf[pos].actorY and len(izquierdo) < actor.count() - 1:
            izquierdo.append(Valor_posicion(posicion=cont + 1, valor=inf[i].valor))
            cont += 1

    cont = 0
    # se realiza la comparacion entre los elementos de derecho e izquierdo para determinar el valor minimo
    for i in range(len(derecho)):
        if izquierdo[cont].posicion == derecho[i].posicion and cont < actor.count():
            if izquierdo[cont].valor <= derecho[i].valor:
                comparacion.append(izquierdo[cont].valor)
            else:
                comparacion.append(derecho[i].valor)
        else:
            cont += 1
            if izquierdo[cont].posicion == derecho[i].posicion:
                if izquierdo[cont].valor <= derecho[i].valor:
                    comparacion.append(izquierdo[cont].valor)
                else:
                    comparacion.append(derecho[i].valor)

    ini = 0  # indica el punto inicial de la sublista
    fin = actor.count()  # indica el punto final de la sublista

    # la lista comparacion es divida y sumada
    for i in range(fin):
        if i < actor.count() - 1:
            # se suman los valores minimos
            lista_suma = map(sum, zip(lista_suma, comparacion[ini:fin]))
            ini = fin  # se actualizan el punto de inicio
            fin = fin + actor.count()  # se actualiza el punto final

    return lista_suma

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Funciones influencias mao>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Generacion de matriz de convergencias o divergencias--------------------------------------------------------->
def generar_caa_daa(lista, actores, cant_objetivos, tipo):
    valores_2mao = []  # valores de la matriz 2mao
    cont = 1
    cont2 = 0

    # filtrado del contenido de la matriz 2mao (solo lo valores de relacion actor x objetivo)
    # al conjunto de valores de una fila se le asigna el una misma posicion para facilitar
    # los filtros y la posterior comparacion
    for i in lista:
        if i.posicion > 0 and i.posicion <= cant_objetivos:
            valores_2mao.append(Valor_posicion(posicion=cont, valor=i.valor))
            cont2 += 1
            if cont2 == cant_objetivos:
                cont += 1
                cont2 = 0

    # Devuelve una lista con los valores que poseen la posicion pasada como parametro
    def filtrar_posicion(pos):
        sublista_aux = []
        for i in valores_2mao:
            if i.posicion == pos:
                sublista_aux.append(i.valor)

        # a la sublista se ingresan los mismos n valores que contiene, hasta que tenga...
        # la misma longitud de la lista que contiene los otros valores con que se ha de comparar
        b = 0
        while len(sublista_aux) < len(valores_2mao) - cant_objetivos:
            sublista_aux.append(sublista_aux[b])
            b += 1
            if b == cant_objetivos:
                b = 0
        return sublista_aux

    # devuelve una lista con los valores con que se ha de comparar la lista retornada por filtrar_posicion
    def filtrar_comparacion(pos):
        sublista_aux = []
        for i in valores_2mao:
            if i.posicion != pos:
                sublista_aux.append(i.valor)
        return sublista_aux

    # Se lleva a cabo el calculo de las convergencias o divergencias de acuerdo al tipo de matriz
    # if tipo == 1 convergencias
    # if tipo == 2 divergencias
    valores = []  # contiene los valores de las convergencias o divergencias calculadas
    pos = 1
    if tipo == 1:
        # Se realiza la comparacion para identificar las convergencias (Signos iguales)
        while pos <= actores.count():
            aux = filtrar_posicion(pos)
            aux2 = filtrar_comparacion(pos)
            cont = 0
            cont2 = 0
            suma = 0
            for i in range(len(aux)):
                # compara si ambos valores son positivos
                if (aux[i] == abs(aux[i])) and (aux2[i] == abs(aux2[i])) and (aux[i] != 0) and (aux2[i] != 0):
                    suma += (aux[i] + aux2[i]) / 2.0
                    cont += 1
                # compara si ambos valores son negativos
                elif (aux[i] != abs(aux[i])) and (aux2[i] != abs(aux2[i])) and (aux[i] != 0) and (aux2[i] != 0):
                    suma += (abs(aux[i]) + abs(aux2[i])) / 2.0
                    cont += 1
                else:
                    cont2 += 1
                if cont + cont2 == cant_objetivos:
                    cont = 0
                    cont2 = 0
                    valores.append(suma)
                    suma = 0
            pos += 1

    else:
        # Se realiza la comparacion para identificar las divergencias (Signos diferentes)
        while pos <= actores.count():
            aux = filtrar_posicion(pos)
            aux2 = filtrar_comparacion(pos)
            cont = 0
            cont2 = 0
            suma = 0
            for i in range(len(aux)):
                # compara si el primero es positivo y el segundo negativo
                if (aux[i] == abs(aux[i])) and (aux2[i] != abs(aux2[i])) and (aux[i] != 0) and (aux2[i] != 0):
                    suma += (aux[i] + abs(aux2[i])) / 2.0
                    cont += 1
                # compara si el primero es negativo y el segundo positivo
                elif (aux[i] != abs(aux[i])) and (aux2[i] == abs(aux2[i])) and (aux[i] != 0) and (aux2[i] != 0):
                    suma += (abs(aux[i]) + aux2[i]) / 2.0
                    cont += 1
                else:
                    cont2 += 1
                if cont + cont2 == cant_objetivos:
                    cont = 0
                    cont2 = 0
                    valores.append(suma)
                    suma = 0
            pos += 1

    # Agregado a la lista de los nombres cortos y de los ceros de la diagonal
    cont = 0
    cont2 = 0
    pos_list = 1
    for i in range(actores.count()):
        # agregado de los nombres cortos de los actores
        valores.insert(cont, actores[i].nombreCorto)
        cont2 = cont + pos_list
        # agregado de los valores 0 de la diagonal
        valores.insert(cont2, 0)
        pos_list += 1
        cont += actores.count() + 1

    # Asignacion de una posicion a cada valor para facilitar la visualizacion de la matriz
    cont = 0
    valores_caa = []
    for i in valores:
        valores_caa.append(Valor_posicion(posicion=cont, valor=i))
        if cont == actores.count():
            cont = 0
        else:
            cont += 1

    if tipo == 1:
        valores_caa.append(Valor_posicion(posicion=0, valor="Ci"))
    else:
        valores_caa.append(Valor_posicion(posicion=0, valor="Di"))

    # Calculo del numero de convergencias o divergencias totales de cada actor
    cont = 1
    suma = 0
    while cont <= actores.count():
        for i in valores_caa:
            if i.posicion == cont:
                suma += i.valor
        valores_caa.append(
            Valor_posicion(posicion="", valor=suma))  # posicion = "" para que no agregue el salto al final
        cont += 1
        suma = 0

    return valores_caa


# View generadora de la matriz 1mao --------------------------------------------------------------------------->
def generar_matriz_mao(tipo):

    objetivo = Objetivo.objects.all().order_by('id')                               # objetivos registrados
    actor = Actor.objects.all().order_by('id')                                     # actores registrados
    mao = Relacion_MAO.objects.exclude(tipo=tipo).order_by('actorY', 'objetivoX')  # relaciones mao registradas
    valores = []                                                                   # valores mostrados en la matriz
    cont = 0                                                                       # cuenta las influencias
    pos_list = 0                                                               # auxiliar para el calculo de cont2
    implicacion = 0     # sumatoria absoluta del lado derecho de la matriz
    movilizacion = 0    # sumatoria absoluta del lado izquierdo de la matriz
    suma_positivos = 0  # sumatoria de los valores positivos de implicacion
    suma_negativos = 0  # sumatoria de los valores negativos de implicacion

    # agregado de las relaciones mao a la lista de valores que sera enviada como contexto
    for i in range(len(mao)):
        cont += 1
        # se agregan las relaciones mao registradas asignandoles una posicion
        valores.append(Valor_posicion(posicion=cont, valor=mao[i].valor))
        # se calcula la sumatoria del valor de implicacion (ultima fila)
        implicacion += abs(mao[i].valor)
        # se determinan las implicaciones positivas y negativas (columnas + y -)
        if mao[i].valor == abs(mao[i].valor):
            suma_positivos += mao[i].valor
        else:
            suma_negativos += abs(mao[i].valor)
            # al agregar los valores correspondientes a una fila se agrega el nombre corto de la siguiente
        if cont == objetivo.count():
            valores.append(Valor_posicion(posicion=cont + 1, valor=suma_positivos))
            valores.append(Valor_posicion(posicion=cont + 2, valor=suma_negativos))
            valores.append(Valor_posicion(posicion=cont + 3, valor=implicacion))
            # determina la posicion donde se va a colocar el nombre corto de la nueva fila
            cont2 = (objetivo.count() + 4) * pos_list
            # inserta el nombre corto de la nueva fila
            valores.insert(cont2, Valor_posicion(posicion=0, valor=actor[pos_list].nombreCorto))
            # reinicio de valores para iterar
            cont = 0
            pos_list += 1
            implicacion = 0
            suma_positivos = 0
            suma_negativos = 0

    # calculo de las sumatorias de movilizacion (3 ultimas filas de la matriz)
    lista_positivos = []
    lista_negativos = []
    lista_movilizacion = []
    cont2 = objetivo.count() + 4  # +4 debido a las cuatro columnas extras en la matriz (nombres cortos y sumatorias)
    cont = 1

    # ---------------------Determinacion de convergencias-------------------->
    valores_caa = generar_caa_daa(valores, actor, objetivo.count(), 1)
    # ---------------------Determinacion de divergencias--------------------->
    valores_daa = generar_caa_daa(valores, actor, objetivo.count(), 2)

    # Determinacion de sumatorias de movilizacion (ultima fila)
    while cont <= objetivo.count():
        for i in valores:
            if i.posicion == cont:
                movilizacion += abs(i.valor)
                if i.valor == abs(i.valor):
                    suma_positivos += i.valor
                else:
                    suma_negativos += abs(i.valor)

        lista_negativos.append(Valor_posicion(posicion=0, valor=suma_negativos))
        lista_positivos.append(Valor_posicion(posicion=0, valor=suma_positivos))
        lista_movilizacion.append(Valor_posicion(posicion=0, valor=movilizacion))
        cont += 1           # iteracion de las posiciones
        movilizacion = 0    # reinicio del valor movilizacion
        suma_positivos = 0  # reinicio de la suma positiva
        suma_negativos = 0  # reinicio de la suma negativa

    # agregado de las sumatorias de movilizacion a la lista de valores a mostrar
    valores.append(Valor_posicion(posicion=0, valor="+"))

    for i in range(len(lista_positivos)):
        valores.append(Valor_posicion(posicion=cont2 + i + 1, valor=lista_positivos[i].valor))

    valores.append(Valor_posicion(posicion=0, valor="-"))

    for i in range(len(lista_negativos)):
        valores.append(Valor_posicion(posicion=cont2 + i + 1, valor=lista_negativos[i].valor))

    valores.append(Valor_posicion(posicion=0, valor="Mov."))

    for i in range(len(lista_movilizacion)):
        valores.append(Valor_posicion(posicion="", valor=lista_movilizacion[i].valor))

    lista = []
    lista.append(objetivo)                # objetivos: lista de objetivos
    lista.append(actor)                   # actores:   lista de actores
    lista.append(valores)                 # valores:   valores de la matriz 2mao
    lista.append(cont2+objetivo.count())  # cantidad de celdas para las filas de movilizacion (ultimas 3 filas)
    lista.append(valores_caa)             # valores_caa: valores de la matriz de convergencias
    lista.append(valores_daa)             # valores_daa: valores de la matriz de divergencias

    return lista

    # funciones de prueba------------------------------------------------------------------------------------------>


# Calculo del valor ri para la matriz 3mao--------------------------------------------------------------------->

def calcular_ri(valores_midi, cant_actor):
    valores_diagonal = []               # valores de la diagonal de la matriz midi
    valores_Ii = []                     # valores Ii de midi
    valores_Di = []                     # valores Di de midi
    valores_ri = []                     # valores ri calculados

    # Se obtienen los valores de la diagonal en la matriz midi
    cont = 0
    cont2 = 0
    for i in valores_midi:
        if i.posicion > 0 and i.posicion <= cant_actor:
            if len(valores_diagonal) == 0 or cont2 + cant_actor == cont:
                valores_diagonal.append(i.valor)
                cont += 1
                cont2 = cont
            else:
                cont += 1
        elif i.posicion == cant_actor+1:
            valores_Ii.append(i.valor)
        elif i.posicion == "":
            valores_Di.append(i.valor)

    suma_ri = 0
    for i in range(len(valores_diagonal)):
        a = valores_Ii[i]
        b = valores_diagonal[i]
        c = valores_Di[cant_actor]
        d = valores_Di[i]
        ri = ((a - b) / (c * 1.0))*(a / ((a + d)*1.0))
        valores_ri.append(ri)
        suma_ri += ri

    ri_prom = suma_ri / cant_actor

    for i in range(len(valores_ri)):
        valores_ri[i] = valores_ri[i] / ri_prom

    return valores_ri


# Calculo de los valores 3mao = 2mao * ri---------------------------------------------------------------------->
def calcular_3mao():

    cant_actor = Actor.objects.count()                                          # cantidad de actores del estudio
    cant_objetivo = Objetivo.objects.count()                                    # cantidad de objetivos del estudio
    mao = Relacion_MAO.objects.exclude(tipo=1).order_by('actorY', 'objetivoX')  # relaciones 2mao registradas
    valores_midi = calcular_midi()                                              # relaciones midi calculadas
    valores_ri = calcular_ri(valores_midi, cant_actor)                          # valores ri a partir de los midi
    valores_3mao = []                                                           # lista que contiene a los 3mao

    # Multiplicacion de los valores 2mao por los valores ri para hallar los 3mao
    cont = 0
    cont2 = 0
    for i in mao:
        if cont2 < cant_objetivo:
            valor = i.valor * valores_ri[cont]
            valores_3mao.append(Valor_posicion(posicion=cont2+1, valor=valor))
            cont2 += 1
        else:
            cont2 = 0
            cont += 1
            valor = i.valor * valores_ri[cont]
            valores_3mao.append(Valor_posicion(posicion=cont2 + 1, valor=valor))
            cont2 += 1

    return valores_3mao


# View generadora de la matriz 3mao --------------------------------------------------------------------------->
def matriz_3mao(request):

        objetivo = Objetivo.objects.all().order_by('id')  # objetivos registrados
        actor = Actor.objects.all().order_by('id')  # actores registrados
        mao = calcular_3mao()
        valores = []  # contiene los valores que se muestran en la matriz
        cont = 0  # cuenta las influencias
        pos_list = 0  # auxiliar para el calculo de cont2
        implicacion = 0  # sumatoria absoluta del lado derecho de la matriz
        movilizacion = 0  # sumatoria absoluta del lado izquierdo de la matriz
        suma_positivos = 0  # sumatoria de los valores positivos de implicacion
        suma_negativos = 0  # sumatoria de los valores negativos de implicacion

        # agregado de las relaciones mao a la lista de valores que sera enviada como contexto
        for i in range(len(mao)):
            cont += 1
            valores.append(Valor_posicion(posicion=cont, valor=mao[i].valor))
            # se calcula la sumatoria del valor de implicacion
            implicacion += abs(mao[i].valor)
            # se determinan las implicaciones positivas y negativas
            if mao[i].valor == abs(mao[i].valor):
                suma_positivos += mao[i].valor
            else:
                suma_negativos += abs(mao[i].valor)
                # al agregar los valores correspondientes a una fila se agrega el nombre corto de la siguiente
            if cont == objetivo.count():
                valores.append(Valor_posicion(posicion=cont + 1, valor=suma_positivos))
                valores.append(Valor_posicion(posicion=cont + 2, valor=suma_negativos))
                valores.append(Valor_posicion(posicion=cont + 3, valor=implicacion))
                # determina la posicion donde se va a colocar el nombre corto de la nueva fila
                cont2 = (objetivo.count() + 4) * pos_list
                # inserta el nombre corto de la nueva fila
                valores.insert(cont2, Valor_posicion(posicion=0, valor=actor[pos_list].nombreCorto))
                # reinicio de valores para iterar
                cont = 0
                pos_list += 1
                implicacion = 0
                suma_positivos = 0
                suma_negativos = 0

        # calculo de las sumatorias de movilizacion (3 ultimas filas de la matriz)
        lista_positivos = []
        lista_negativos = []
        lista_movilizacion = []
        cont2 = objetivo.count() + 4  # +4 debido a las cuatro columnas extras en la matriz (nombres cortos y sumatorias)
        cont = 1

        # ---------------------Determinacion de convergencias-------------------->
        valores_caa = generar_caa_daa(valores, actor, objetivo.count(), 1)
        # ---------------------Determinacion de divergencias--------------------->
        valores_daa = generar_caa_daa(valores, actor, objetivo.count(), 2)

        # Determinacion de sumatorias de movilizacion (ultima fila)
        while cont <= objetivo.count():
            for i in valores:
                if i.posicion == cont:
                    movilizacion += abs(i.valor)
                    if i.valor == abs(i.valor):
                        suma_positivos += i.valor
                    else:
                        suma_negativos += abs(i.valor)

            lista_negativos.append(Valor_posicion(posicion=0, valor=suma_negativos))
            lista_positivos.append(Valor_posicion(posicion=0, valor=suma_positivos))
            lista_movilizacion.append(Valor_posicion(posicion=0, valor=movilizacion))
            cont += 1  # iteracion de las posiciones
            movilizacion = 0  # reinicio del valor movilizacion
            suma_positivos = 0  # reinicio de la suma positiva
            suma_negativos = 0  # reinicio de la suma negativa

        # agregado de las sumatorias de movilizacion a la lista de valores a mostrar
        valores.append(Valor_posicion(posicion=0, valor="+"))

        for i in range(len(lista_positivos)):
            valores.append(Valor_posicion(posicion=cont2 + i + 1, valor=lista_positivos[i].valor))

        valores.append(Valor_posicion(posicion=0, valor="-"))

        for i in range(len(lista_negativos)):
            valores.append(Valor_posicion(posicion=cont2 + i + 1, valor=lista_negativos[i].valor))

        valores.append(Valor_posicion(posicion=0, valor="Mov."))

        for i in range(len(lista_movilizacion)):
            valores.append(Valor_posicion(posicion="", valor=lista_movilizacion[i].valor))

        print cont2

        # objetivos: lista de objetivos
        # actores:   lista de actores
        # valores:   valores de la matriz 2mao
        # cantidad:  cantidad de columnas, ayuda a establecer cuando hacer el salto de fila
        # cantidad2: cantidad de columnas para las sumatorias de movilizacion (ultimas 3 filas)
        # valores_caa: valores de la matriz de convergencias
        # valores_daa: valores de la matriz de divergencias

        contexto = {'objetivos': objetivo, 'actores': actor, 'valores': valores, 'cantidad': objetivo.count() + 3,
                    'cantidad2': cont2 + objetivo.count(), 'valores_caa': valores_caa, 'cantidad3': actor.count(),
                    'valores_daa': valores_daa}
        return render(request, 'mao/matriz_3mao.html', contexto)


#------------------------------------VIEWS AJAX----------------------------------------------------

# Obtiene la descripcion del actor seleccionado
def actor_ajax(request):

    if request.is_ajax():
        actor = Actor.objects.get(id=request.GET['id'])
        response = JsonResponse({'descripcion': actor.descripcion})
        return HttpResponse(response.content)
    else:
        return redirect('/')# redirecciona a la misma pagina


# Obtiene la descripcion del objetivo seleccionado
def consultar_desc_obj(request):

    if request.is_ajax():
        objetivo = Objetivo.objects.get(id=request.GET['id'])
        response = JsonResponse({'descripcion': objetivo.descripcion})
        return HttpResponse(response.content)
    else:
        return redirect('/')

# Obtiene la ficha de influencias del par de actores seleccionado
def consultar_ficha(request):

    if request.is_ajax():
        if request.GET['id'] == "" or request.GET['id2'] == "":
            response = JsonResponse({'info': "Seleccione el par de actores a consultar"})
            return HttpResponse(response.content)
        else:
            ficha = Ficha_actor.objects.get(actorX=request.GET['id'], actorY=request.GET['id2'])
            response = JsonResponse({'info': ficha.info})
            return HttpResponse(response.content)

    else:
        return redirect('/')  # redirecciona a la misma pagina


def consultar_comentarios(request):

    if request.is_ajax():
        inf = Relacion_Influencia.objects.get(actorX=request.GET['id'], actorY=request.GET['id2'])
        response = JsonResponse({'justificacion': inf.justificacion})
        return HttpResponse(response.content)
    else:
        return redirect('/')  # redirecciona a la misma pagina


def index(request):
    return render(request, 'index.html')


def prueba(request):
    return render(request, 'baseForms/base_forms.html')
