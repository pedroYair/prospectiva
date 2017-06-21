from django.contrib import admin
from .models import Estudio_Mactor, Actor, Ficha, Objetivo, Relacion_Influencia, Relacion_MAO, Cuestion_Estrategica, Informe_Final

# Register your models here.
#El modelo admin permite visualizar los campos especificados en forma de tabla en el administrador

# ---------------------------------------------------------------------------
class EstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_final', 'estado')

admin.site.register(Estudio_Mactor, EstudioAdmin)

# -------------------------------------------------------------------------
class ActorAdmin(admin.ModelAdmin):
    list_display = ('nombreCorto', 'nombreLargo', 'descripcion')
    ordering = ('nombreLargo',)

admin.site.register(Actor, ActorAdmin)

#--------------------------------------------------------------------------
class FichaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'objetivos', 'preferencias')


admin.site.register(Ficha, FichaAdmin)

# -------------------------------------------------------------------------
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ('nombreCorto', 'nombreLargo', 'descripcion')
    ordering = ('nombreLargo',)

admin.site.register(Objetivo, ObjetivoAdmin)

# -------------------------------------------------------------------------
admin.site.register(Relacion_Influencia)
admin.site.register(Relacion_MAO)
admin.site.register(Cuestion_Estrategica)
admin.site.register(Informe_Final)



