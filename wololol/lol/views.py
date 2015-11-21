 #Al quitar alguna linea al trabajar, transformenla en un comentario con 3 numerales
import json
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from chat import Cliente
from riotwatcher import getApiSummoner, getCacheSummoner
#from ovejawatcher import getSummoner, prueba

#ReturnJSON: return HttpResponse(json.dumps(valores), content_type="application/json")


def profile(request, summoner = None, idSum = None, region = None, info = None):
    context = RequestContext(request)
    #si todo none, mostrar buscador
    #si server e id/summoner, pedir get cache summoner
    #si getCacheSummoner == None pedir api summoner
    #getApiSummoner y reemplazar las variables en el html
    # if request.method == "POST":
    #     print(summoner, idSum, region, info)
    #     info = getApiSummoner(summoner = summoner, idSum = idSum, region = region)
    #     return HttpResponse(json.dumps(info), content_type="application/json")
    info = getApiSummoner(summoner = 'Sad Jocker King', region = 'las')
    #info = prueba(summonerId=426174)
    return render_to_response('profile.html', {"info":info}, context)

def chat(request, user = None, password = None, region = None, friend = None):
    if user != None and password != None and region != None:
        cliente = Cliente(user, password, region)
    else:
        cliente = Cliente("banersjk", "zxmfkmk126", "las")
    import time
    print("ESPERANDO 20 SECONDS")
    time.sleep(5)
    info = cliente.getAll()

    #cliente.send("421651", "Hola como andas?")#Envia Mensaje al summoner con esa id
    #cliente.statusMsg = "Mensaje de Estado Nuevo"#modifica una propiedad del cliente
    #cliente.refreshStatusFromProps()#Y refresca el estado online con esa nueva propiedad
    info = None
    context = RequestContext(request)
    return render_to_response('chat.html', {"info":info}, context)


#TODO cambiar nombre static
def static(request, section = None, specific = None):
    print("#-----static-----#")

def home(request):
    context = RequestContext(request)
    return render_to_response('home.html', context)
