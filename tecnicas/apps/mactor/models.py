# coding=utf-8
from django.contrib.auth.models import User
from django.db import models


# MODELO ESTUDIO MACTOR----------------------------------------------------------------------->

class Estudio_Mactor(models.Model):
    codigo = models.PositiveIntegerField(default=1)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    coordinadores = models.ManyToManyField('auth.User',
                                           verbose_name='Coordinadores',
                                           related_name='mactor_coordinadores_set')
    expertos = models.ManyToManyField('auth.User',
                                      verbose_name='Expertos',
                                      related_name='mactor_expertos_set')
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    codigo_proy = models.PositiveIntegerField(default=1)

# Definicion de nombre singular y plurar del modelo
    class Meta:
        verbose_name = 'Estudio_Mactor'
        verbose_name_plural = 'Estudios_Mactor'

# Campo a mostrar del modelo Estudio_Mactor
    def __unicode__(self):
        return u'{0} - {1} - {2} - {3}'.format(self.titulo, self.fecha_inicio, self.fecha_final, self.estado)

# MODELO ACTOR: FASE 1 - LISTA DE ACTORES----------------------------------------------------->


class Actor(models.Model):
    nombreLargo = models.CharField(max_length=50)
    nombreCorto = models.CharField(max_length=10)
    descripcion = models.TextField(blank=True, null=True)
    codigo_Estudio = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actores'

    def __unicode__(self):
        return u'{0} - {1}'.format(self.nombreCorto, self.nombreLargo)

# MODELO OBJETIVO: FASE 2 - LISTA DE OBJETIVOS------------------------------------------------>

class Ficha_actor(models.Model):
    actorY = models.ForeignKey(Actor, null=True, blank=False, related_name='mactor_actorY_ficha')
    actorX = models.ForeignKey(Actor, null=True, blank=False, related_name='mactor_actorX_ficha')
    info = models.TextField(null=True, blank=True)
    creador = models.ForeignKey(User, null=True)
    codigo_Estudio = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Ficha_actor'
        verbose_name_plural = 'Fichas_actores'
        # para evitar que la pareja de registros se repita en ese mismo orden
        unique_together = ('actorY', 'actorX', 'creador')


    def __unicode__(self):
        return u'{0} - {1} - {2}'.format(self.actorY, self.actorX, self.info)


class Objetivo(models.Model):
    nombreLargo = models.CharField(max_length=50)
    nombreCorto = models.CharField(max_length=10)
    descripcion = models.TextField(blank=True, null=True)
    codigo_Estudio = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Objetivo'
        verbose_name_plural = 'Objetivos'

    def __unicode__(self):
        return u'{0} - {1}'.format(self.nombreCorto, self.nombreLargo)

# MODELO INFLUENCIAS MID---------------------------------------------------------------------->


class Relacion_Influencia(models.Model):
    actorX = models.ForeignKey(Actor, null=True, blank=False, related_name='mactor_actorX_set')
    actorY = models.ForeignKey(Actor, null=True, blank=False, related_name='mactor_actorY_set')
    valor = models.IntegerField()
    justificacion = models.TextField(null=True, blank=True)
    creador = models.ForeignKey(User, null=True)
    codigo_Estudio = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Relacion_de_Influencia'
        verbose_name_plural = 'Relaciones_de_influencia'
        # para evitar que la pareja de registros se repita en ese mismo orden
        unique_together = ('actorX', 'actorY', 'creador')


    def __unicode__(self):
        return u'{0} - {1} - {2}'.format(self.actorY, self.actorX, self.valor)


# MODELO RELACIONES MAO : ACTORES X OBJETIVOS---------------------------------------------->

class Relacion_MAO(models.Model):
    tipo = models.IntegerField(null=True, blank=True)
    actorY = models.ForeignKey(Actor, null=False, blank=False, on_delete=models.CASCADE)
    objetivoX = models.ForeignKey(Objetivo, null=False, blank=False, on_delete=models.CASCADE)
    valor = models.IntegerField()
    justificacion = models.TextField(max_length=50, null=True, blank=True)
    creador = models.ForeignKey(User, null=True)
    codigo_Estudio = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Relacion_MAO'
        verbose_name_plural = 'Relaciones_MAO'
        unique_together = ('tipo', 'actorY', 'objetivoX', 'creador')

    def __unicode__(self):
        return u'{0} - {1} - {2} - {3} - {4}'.format(self.tipo, self.actorY, self.objetivoX, self.valor, self.creador)


# MODELO CUESTION ESTRATEGICA--------------------------------------------------------------->

class Cuestion_Estrategica(models.Model):
    actor = models.ForeignKey(Actor, null=True, blank=True)
    cuestion = models.TextField(max_length=200)
    creador = models.ForeignKey(User, null=True)
    codigo_Estudio = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Cuestion_estrategica'
        verbose_name_plural = 'Cuestiones_estrategicas'

    def __unicode__(self):
        return u'{0} - {1} - {2}- {3}'.format(self.actor, self.cuestion, self.creador, self.codigo_Estudio)


# MODELO INFORME FINAL ---------------------------------------------------------------------->

class Informe_Final(models.Model):
    codigo = models.IntegerField()
    fecha = models.DateField(auto_now=True)
    informe = models.TextField()
    cuestiones = models.ForeignKey(Cuestion_Estrategica, null=True, blank=True)
    creador = models.ForeignKey(User, null=True)
    codigo_Estudio = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Informe_final'
        verbose_name_plural = 'Informes_finales'

    def __unicode__(self):
        return u'{0} - {1} - {2}'.format(self.codigo_Estudio, self.fecha, self.informe, self.cuestiones, self.creador)
