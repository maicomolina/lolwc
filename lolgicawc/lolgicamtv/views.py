

from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

from itertools import groupby as g

from riotwatcher import LATIN_AMERICA_SOUTH
from riotwatcher import RiotWatcher
from riotwatcher import LoLException

# Create your views here.

riotWatcher = RiotWatcher("98f4f837-c794-4a58-bcb7-b436873a03d2", default_region=LATIN_AMERICA_SOUTH)
i = 0

def home(request):
    x = 0
    free_to_play = True
    context = RequestContext(request)
    #-->Nombre Summoner
    me = riotWatcher.get_summoner(name='sadjockerking')
    nombre = me['name']
#426174
    try:
        #-->Liga
        ligaInfo = riotWatcher.get_league_entry([str(me['id'])])
        liga = ligaInfo['426174'][0]['tier']
        #-->Division
        division = ligaInfo['426174'][0]['entries'][0]['division']
    except(LoLException):
        #-->En caso de no rankear
        liga = "unRanked"
        division = "unRanked"
    try:
        #-->Info como le va en rankeds
        summary = riotWatcher.get_stat_summary(me['id'])
        
        for x in range(len(summary['playerStatSummaries'])):
            if (summary['playerStatSummaries'][x]['playerStatSummaryType'] == "RankedSolo5x5" ):
                break
        kills = summary['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        assists = summary['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        wins = summary['playerStatSummaries'][x]['wins']
        losses = summary['playerStatSummaries'][x]['losses']
    except(IndexError):
        kills = '0'
        assists = '0'
        wins = '0'
        losses = '0'
    
    #-->Free Champs
    freeChamps = riotWatcher.get_all_free_champions()
    freeChampsID = []
    for j in range(len(freeChamps['champions'])):
        freeChampsID.append(freeChamps['champions'][j]['id'])
        
    #-->Partidas
    tiempoSec = [0,0,0,0,0]
    minutos = [0,0,0,0,0]
    segundos = [0,0,0,0,0]
    champPartida = []
    try:
        for k in range(5):
            champFGc = []
            champFGd = []
            partida = riotWatcher.get_featured_games()
            tiempoSec[k] = partida['gameList'][k]['gameLength']
            minutos[k] = tiempoSec[k] /60
            segundos[k] =  tiempoSec[k]%60
            for u in range (len(partida['gameList'][k]['participants'])):
                if partida['gameList'][k]['participants'][u]['teamId'] == 100 :
                    champFGc.append(partida['gameList'][k]['participants'][u]['championId'])
                else:
                    champFGd.append(partida['gameList'][k]['participants'][u]['championId'])
            champPartida.append(champFGd)
            champPartida.append(champFGc)
    except (LoLException):
        print 'mierda'




    return render_to_response('home.html', {'nombre':nombre, 'liga':liga, 'division':division,
                                            'kills':kills, 'assists':assists,
                                            'wins':wins, 'losses':losses,
                                            'freeChampsID':freeChampsID, 'minutos':minutos,
                                            'segundos':segundos,
                                            'champFGc':champFGc, 'champFGd':champFGd, 'champPartida':champPartida,
                                            }, 
                             context)

def most_common(L):
  return max(g(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]