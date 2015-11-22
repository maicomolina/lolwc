 #Al quitar alguna linea al trabajar, transformenla en un comentario con 3 numerales
import json
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from chat import Cliente
from riotwatcher import getApiSummoner, getCacheSummoner
###from ovejawatcher import getSummoner, prueba

#ReturnJSON: return HttpResponse(json.dumps(valores), content_type="application/json")

clientes = []

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
    ###info = prueba(summonerId=426174)
    return render_to_response('profile.html', {"info":info}, context)

def chat(request, user = None, password = None, region = None, friend = None):
    #TODO iniciar chat cuando me logueo
    #TODO darle al client.py capacidades de renderizar
    #TODO enviar json con la informacion de getAll y printearla por python
    #TODO printear la informacion json por javascript
    #TODO loguearme con el chatoff
    #TODO iniciar socket por javascript y el client, que el client le renderize al socket
    context = RequestContext(request)
    if user != None and password != None and region != None:
        cliente = Cliente(user, password, region)
    else:
        print("Returnear pagina de error de forma similar a lo comentado abajo")
        #info = {"head":"No ingreso todos los datos", "content":"Asegurese de ingresar los datos correctamente"}
        #return render_to_response('error.html',{"info":info}, context)
        return render_to_response('chatOff.html', context)

    return render_to_response('chat.html', context)


#TODO cambiar nombre static
def data(request, section = None, specific = None):
    print("#----data----#")
    context = RequestContext(request)
    return render_to_response('underConstruction.html', context)

def home(request):
    context = RequestContext(request)
    return render_to_response('home.html', context)
