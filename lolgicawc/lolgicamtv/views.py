

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
    context = RequestContext(request)

    me = riotWatcher.get_summoner(name='sadjockerking')
    nombre = me['name']
#426174
    try:
        ligaInfo = riotWatcher.get_league_entry([str(me['id'])])
        liga = ligaInfo['426174'][0]['tier']
        division = ligaInfo['426174'][0]['entries'][0]['division']
    except(LoLException):
        liga = "unRanked"
        division = "unRanked"
    try:
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
    
    listaP = riotWatcher.get_match_list(me['id'])
    champList = []
    for i in range(listaP['totalGames']):
        champ = listaP['matches'][i]['champion']
        champList.append(champ)
    print most_common(champList)

    return render_to_response('home.html', {'nombre':nombre, 'liga':liga, 'division':division,
                                            'kills':kills, 'assists':assists,
                                            'wins':wins, 'losses':losses
                                           }, 
                             context)

def most_common(L):
  return max(g(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]