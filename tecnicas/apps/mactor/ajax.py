from django.http import JsonResponse

from .models import Actor


def eliminar_actor(request):
    pk = request.POST.get('id')
    id = Actor.objects.get(pk=pk)
    id.delete()
    response = {}
    return JsonResponse(response)