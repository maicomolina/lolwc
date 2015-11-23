#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from ovejawatcherFinal import getSummoner, getApiHistory
#from chat import Cliente
###from riotwatcher import getApiSummoner, getCacheSummoner

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
    #info = getSummoner(summoner = 'ISG HyperX Emp', region = 'las')
    info = getApiHistory(idSum=426174)
    return render_to_response('profile.html', {"info":info}, context)

def send_hello_world():#BORRAMEBORRAMEBORRAMEBORRAMEBORRAMEBORRAMEBORRAMEBORRAMEBORRAMEBORRAME
    from omnibus.api import publish
    print("helloworld?")
    publish(
        'chat',  # the name of the channel
        'friendConnected',  # the `type` of the message/event, clients use this name to register event handlers
        {'text': 'Hello world'},  # payload of the event, needs to be a dict which is JSON dumpable.
        sender='server'  # sender id of the event, can be None.
    )

def chat(request, user = None, password = None, region = None, friend = None):
    send_hello_world()#BORRAMEBORRAMEBORRAMEBORRAMEBORRAMEBORRAMEBORRAMEBORRAMEBORRAMEBORRAME
    context = RequestContext(request)
    global clientes
    #TODO iniciar chat cuando me logueo
    #me logueo bien por html
    #me logueo bien por url
    #me logueo mal por html
    #me logueo mal por url
    #TODO darle al client.py capacidades de renderizar
    #TODO que el client renderice los errores de auth y de conexion
    #TODO enviar json con la informacion de getAll y printearla por python
    #TODO printear la informacion json por javascript
    #TODO loguearme con el chatoff
    #TODO iniciar socket por javascript y el client, que el client le renderize al socket
    if request.method == "POST":
        region = request.POST["server"]
        user = request.POST["user"]
        password = request.POST["password"]

    if user != None and password != None and region != None:
        cliente = Cliente(user, password, region)
        if cliente.connected:
            for i in range(len(clientes)):
                if clientes[i].jid == cliente.jid:
                    clientes.pop(i)
                    break
            clientes.append(cliente)
            info={
                #TODO returnear serverStatus
                "message":"<h1 class='green-text'>Conectando...</h1><p class='center white-text'>Espere mientras se conecta al servidor de Riot Games</p>",
                "typ":"loginCorrect"
                }
            if request.method == "POST":
                return HttpResponse(json.dumps(info), content_type="application/json")
            return render_to_response('chat.html', {"info":info}, context)

        else:
            info={
                #TODO returnear serverStatus
                "message":"<h1 class='red-text'>No fue posible conectarse</h1><p class='center red-text'>Revisa tu usario y contraseña</p>",
                "typ":"authError",
                }
            if request.method == "POST":
                return HttpResponse(json.dumps(info), content_type="application/json")
            return render_to_response('chat.html', {"info":info}, context)
    else:
        return render_to_response('chat.html', context)

#TODO cambiar nombre static
def data(request, section = None, specific = None):
    print("#----data----#")
    context = RequestContext(request)
    return render_to_response('underConstruction.html', context)

def home(request):
    context = RequestContext(request)
    return render_to_response('home.html', context)
