# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from .models import Actor, Ficha_actor, Objetivo, Estudio_Mactor, Relacion_Influencia, Relacion_MAO
from .choices import VALORES, VALORES_1MAO, VALORES_2MAO


# FORMULARIO DE ESTUDIO MACTOR----------------------------------------------------------------------------------------->

class Formulario_Estudio(forms.ModelForm):
    def clean_titulo(self):
        mensaje = self.cleaned_data["titulo"]
        palabras = len(mensaje.split())
        if palabras < 2:
            raise forms.ValidationError(u"Ingrese mínimo dos palabras para el título")
        return mensaje

    class Meta:
        model = Estudio_Mactor

        fields = [
            'codigo',
            'titulo',
            'descripcion',
            'coordinadores',
            'expertos',
            'fecha_inicio',
            'fecha_final',
            'estado',
            'codigo_proy',
        ]

        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'coordinadores': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'expertos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker'}),
            'fecha_final': forms.DateInput(attrs={'class': 'datepicker'}),
            'estado': forms.CheckboxInput(),
            'codigo_proy': forms.TextInput(attrs={'class': 'form-control'}),
        }

# FORMULARIO DE ACTOR-------------------------------------------------------------------------------------------------->

class Formulario_actor(forms.ModelForm):

    def clean_nombreCorto(self):
        act = Actor.objects.all()
        nombre = self.cleaned_data['nombreCorto']

        for i in act:
            if i.nombreCorto == nombre:
                raise forms.ValidationError('Ya existe un actor con este nombre corto')
            else:
                return nombre

    def clean_nombreLargo(self):
        act = Actor.objects.all()
        nombre = self.cleaned_data['nombreLargo']
        palabras = len(nombre.split())

        for i in act:
            if i.nombreLargo == nombre:
                raise forms.ValidationError('Ya existe un actor con este nombre largo')
            elif palabras < 2:
                raise forms.ValidationError(u"Se requieren mínimo dos palabras para el nombre largo")
            else:
                return nombre

    # la clase meta especifica de que modelo se va hacer el formulario
    class Meta:
        model = Actor

        fields = [
            'nombreLargo',
            'nombreCorto',
            'descripcion',
            'codigo_Estudio',
        ]

        widgets = {
            'nombreLargo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombreCorto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'row': '3', 'placeholder': u'Ingrese información '
                         'relacionada a objetivos, preferencias, motivaciones, propuestas, comportamientos o recursos del actor.'}),
            'codigo_Estudio': forms.TextInput(attrs={'class': 'form-control'}, ),
        }

# FORMULARIO FICHA DEL ACTOR

class Formulario_Ficha(forms.ModelForm):

    class Meta:
        model = Ficha_actor

        fields = [
            'actorX',
            'actorY',
            'info',
            'creador',
            'codigo_Estudio',
        ]

        widgets = {
            'actorX': forms.Select(attrs={'class': 'form-control'}),
            'actorY': forms.Select(attrs={'class': 'form-control'}),
            'info': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'creador': forms.Select(attrs={'class': 'form-control'}),
            'codigo_Estudio': forms.TextInput(attrs={'class': 'form-control'}, ),
        }

# FORMULARIO DE OBJETIVO----------------------------------------------------------------------------------------------->

class Formulario_objetivo(forms.ModelForm):

    def clean_nombreLargo(self):
        obj = Objetivo.objects.all()
        nombre = self.cleaned_data['nombreLargo']
        palabras = len(nombre.split())

        for i in obj:
            if i.nombreLargo == nombre:
                raise forms.ValidationError('Ya existe un objetivo con este nombre largo')
            elif palabras < 2:
                raise forms.ValidationError(u"Se requieren mínimo dos palabras para el nombre largo")
            else:
                return nombre

    def clean_nombreCorto(self):
        obj = Objetivo.objects.all()
        nombre = self.cleaned_data['nombreCorto']

        for i in obj:
            if i.nombreCorto == nombre:
                raise forms.ValidationError('Ya existe un objetivo con este nombre corto')
        else:
            return nombre

    class Meta:
        model = Objetivo
        #         exclude = ('creador',)
        fields = [
            'nombreLargo',
            'nombreCorto',
            'descripcion',
            'codigo_Estudio',
        ]

        labels = {
            'nombreLargo': 'Nombre Largo',
            'nombreCorto': 'Nombre Corto',
            'descripcion': 'Descripcion',
            'codigo_Estudio': 'Codigo Estudio',
        }

        widgets = {
            'nombreLargo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombreCorto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'codigo_Estudio': forms.TextInput(attrs={'class': 'form-control'}, ),
        }


# FORMULARIO DE INFLUENCIAS-------------------------------------------------------------------------------------------->

class Formulario_Influencia(forms.ModelForm):

    def clean_actorY(self):
        actor1 = self.cleaned_data['actorX']
        actor2 = self.cleaned_data['actorY']
        if actor1 == actor2:
            raise forms.ValidationError(u'Un actor no tiene influencia sobre sí mismo')
        else:
            return actor2

    class Meta:
        model = Relacion_Influencia

        fields = [
            'actorX',
            'actorY',
            'valor',
            'justificacion',
            'creador',
            'codigo_Estudio',
        ]

        widgets = {
            'actorX': forms.Select(attrs={'class': 'form-control'}),
            'actorY': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.Select(choices=VALORES, attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'creador': forms.Select(attrs={'class': 'form-control'}),
            'codigo_Estudio': forms.TextInput(attrs={'class': 'form-control'}, ),
        }

# FORMULARIO 1MAO------------------------------------------------------------------------------------------------------>

class Formulario_1mao(forms.ModelForm):

    class Meta:
        model = Relacion_MAO

        fields = [
            'tipo',
            'actorY',
            'objetivoX',
            'valor',
            'justificacion',
            'creador',
            'codigo_Estudio',
            ]

        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'actorY': forms.Select(attrs={'class': 'form-control'}),
            'objetivoX': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.Select(choices=VALORES_1MAO, attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'creador': forms.Select(attrs={'class': 'form-control'}),
            'codigo_Estudio': forms.TextInput(attrs={'class': 'form-control'}, ),
            }

# FORMULARIO 2MAO------------------------------------------------------------------------------------------------------>

class Formulario_2mao(forms.ModelForm):

    class Meta:
        model = Relacion_MAO

        fields = [
            'tipo',
            'actorY',
            'objetivoX',
            'valor',
            'justificacion',
            'creador',
            'codigo_Estudio',
        ]

        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'actorY': forms.Select(attrs={'class': 'form-control'}),
            'objetivoX': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.Select(choices=VALORES_2MAO, attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'creador': forms.Select(attrs={'class': 'form-control'}),
            'codigo_Estudio': forms.TextInput(attrs={'class': 'form-control'}, ),
        }
