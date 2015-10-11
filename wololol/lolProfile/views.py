import json

from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

from itertools import groupby as g

from riotwatcher import LATIN_AMERICA_SOUTH
from riotwatcher import RiotWatcher
from riotwatcher import LoLException

    # context = RequestContext(request)
    # if request.method == 'POST':
    #     nombre = request.POST['nombre']
    #     mensaje = request.POST['mensaje']
    #     id_post = request.POST['id']
    #     comentario = Comentario()
    #     comentario.mensaje = mensaje
    #     comentario.nombre = nombre
    #     comentario.entrada = Entrada.objects.get(id=id_post)
    #     comentario.save()
    #     comentarioReturn = {"nombre": comentario.nombre, "fecha": "Ahora", "mensaje":comentario.mensaje}
    # 	return HttpResponse(json.dumps(comentarioReturn), content_type="application/json")
riotWatcher = RiotWatcher("98f4f837-c794-4a58-bcb7-b436873a03d2", default_region=LATIN_AMERICA_SOUTH)
i = 0
def profile(request, summoner = None, idSum = None, region = None, info = None):
    context = RequestContext(request)
    if request.method == 'POST':
        valores = {}
        if request.POST["value"] == "summonerInfo":
            valores = summonerInfo(summoner)
            print(valores)
        print(valores)
        return HttpResponse(json.dumps(valores), content_type="application/json")
    return render_to_response('profile.html',{"summoner":summoner,"idSum":idSum,"region":region,"info":info},context)


def chat(request, region = None, friend = None):
    print("#-----chat-----#")
def static(request, section = None, specific = None):
    print("#-----static-----#")
def home(request, section = None, specific = None):
    print("#-----static-----#")

def summonerInfo(summoner):
    print("name:"+str(summoner))
    wins = 0
    losses = 0
    assists = 0
    kills = 0
    deaths = 0
    free_to_play = True
    #-->Nombre Summoner

    me = riotWatcher.get_summoner(name=summoner)
    nombre = me['name']

    #426174
    try:
        #-->Liga
        ligaInfo = riotWatcher.get_league_entry([str(me['id'])])
        liga = ligaInfo[str(me['id'])][0]['tier']
        #-->Division
        division = ligaInfo[str(me['id'])][0]['entries'][0]['division']

    except(LoLException):
        #-->En caso de no rankear
        liga = "unRanked"
        division = "unRanked"
        try:
            #-->Info como le va en rankeds
            rankedst = riotWatcher.get_ranked_stats(me['id'])

            for x in range(len(rankedst['champions'])):
                wins += rankedst['champions'][x]['stats']['totalSessionsWon']
                losses += rankedst['champions'][x]['stats']['totalSessionsLost']
                assists += rankedst['champions'][x]['stats']['totalAssists']
                kills += rankedst['champions'][x]['stats']['totalChampionKills']
                deaths += rankedst['champions'][x]['stats']['totalDeathsPerSession']
        except(IndexError, LoLException):
            kills = '0'
            assists = '0'
            wins = '0'
            losses = '0'
            deaths = '0'
    print("PATAASOOOOOOOOOOOOOO")


    res = {"mostPlayedChampBannerImg":"NOLOTENGO","summonerImg":"NOLOTENGO",
"summonerName":str(nombre),"summonerLeagueImg":"NOLOTENGO","summonerLeagueName":str(liga)+" "+str(division),
"summonerServer":"NOLOTENGO","summonerKills":str(kills),"summonerDeaths":str(deaths),
"summonerAssist":str(assists),"summonerKdaRatio":"NOLOTENGO","summonerWinrate":"Wins:"+str(wins)}
    return res
    # return {'nombre':nombre, 'liga':liga, 'division':division,
    # 'kills':kills, 'assists':assists,
    # 'deaths':deaths,
    # 'wins':wins, 'losses':losses,}
