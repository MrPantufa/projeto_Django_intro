import asyncio
from django.http import JsonResponse
from django.shortcuts import render

def index(request):
    return render(request, "index.html")

async def async_tick(request):
    # espera 1 segundo de forma não bloqueante e retorna um JSON
    await asyncio.sleep(1)
    return JsonResponse({'ok': True})

async def contador_page(request):
    # página que mostra o contador, acionando o endpoint assíncrono
    return render(request, "contador.html", {'segundos': int(request.GET.get('segundos', 10))})
