from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

from riotwatcher import LATIN_AMERICA_SOUTH
from riotwatcher import RiotWatcher
from riotwatcher import LoLException
from dataRunes import dataRunes


# Create your views here.
''' Aqui esta toda la logica de todos los pedidos a la API de league Of Leagends. Por temas de 
comodidad se utilizo la herramienta Riot Watcher, sirve para hacer los pedidos mediante funciones
de Python.'''
riotWatcher = RiotWatcher("98f4f837-c794-4a58-bcb7-b436873a03d2", default_region=LATIN_AMERICA_SOUTH)
me = riotWatcher.get_summoner(name='sadjockerking')#Se le agradece a Sad Jocker King por prestar su cuenta
try:
    rankedst = riotWatcher.get_ranked_stats(me['id'])
    x = int(len(rankedst['champions'])) - 1
except(LoLException):
    rankedst = {}
    x = 0

def home(request):
    free_to_play = True
    context = RequestContext(request)
#    sumInf = summonerInfo()
#    mpcInf = mostPlayedChampInfo()
#    featgames = featuredGames()
#    free = freeChamps()
#    his = history()
    totalInfo = {}
    runas = runes()
#    maestrias = masteries()
#    ligas = league()
    
    # De esta forma los datos ingresan de forma organizada al diccionario con la informacion total
    
#    for ii in sumInf:
#        totalInfo[ii] = sumInf[ii]
#    for jj in mpcInf:
#        totalInfo[jj] = mpcInf[jj]
#    for oo in featgames:
#        totalInfo[oo] = featgames[oo]
#    for pp in his:
#        totalInfo[pp] = his[pp]
#    for cc in free:
#        totalInfo[cc] = free[cc]
    for qq in runas:
        totalInfo[qq] = runas[qq]
#    for mm in maestrias:
#        totalInfo[mm]  = maestrias[mm]
#    for ll in ligas:
#        totalInfo[ll]  = ligas[ll]
        
    return render_to_response('home.html', totalInfo )
#426174
#-- Informacion del summoner
def summonerInfo():
    try:
        summonerName = me['name']
        ligaInfo = riotWatcher.get_league_entry([str(me['id'])])
        #-->Liga
        summonerLeage = ligaInfo[str(me['id'])][0]['tier']
        #-->Division
        summonerDivision = ligaInfo[str(me['id'])][0]['entries'][0]['division']
    except(LoLException):
        #-->En caso de no rankear
        summonerLeage = "unRanked"
        summonerDivision = "unRanked"
    try:
            #-->Info como le va en rankeds
        summonerAssists = 0.0
        summonerKills = 0.0
        summonerDeaths = 0.0
        wins = rankedst['champions'][x]['stats']['totalSessionsWon']
        losses = rankedst['champions'][x]['stats']['totalSessionsLost']
        summonerAssists = rankedst['champions'][x]['stats']['totalAssists']/ rankedst['champions'][x]['stats']['totalSessionsPlayed']
        summonerKills = rankedst['champions'][x]['stats']['totalChampionKills'] / rankedst['champions'][x]['stats']['totalSessionsPlayed']
        summonerDeaths = rankedst['champions'][x]['stats']['totalDeathsPerSession']/ rankedst['champions'][x]['stats']['totalSessionsPlayed']
        totalPartidas = wins + losses
        summonerWinrate = totalPartidas*wins/losses
    except(IndexError, LoLException, KeyError):
        summonerKills = '0'
        summonerAssists = '0'
        wins = '0'
        losses = '0'
        summonerDeaths = '0'
    summonerInf = {}
    summonerInf['summonerName'] = summonerName
    summonerInf['summonerLeage'] = summonerLeage
    summonerInf['summonerDivision'] = summonerDivision
    summonerInf['summonerKills'] = summonerKills
    summonerInf['summonerAssists'] = summonerAssists
    summonerInf['summonerDeaths'] = summonerDeaths
    summonerInf['summonerWinrate'] = summonerWinrate
    return summonerInf


#-->Champion mas usado
def mostPlayedChampInfo():

    try:
        champWinPorcentaje = 0.0
        mostPlayedChampMatchesCount =  0
        mostPlayedChamp = 0
        for q in range(x):
            partidaChampx = rankedst['champions'][q]['stats']['totalSessionsPlayed']
            if (mostPlayedChampMatchesCount <= partidaChampx):
                mostPlayedChampMatchesCount = partidaChampx
                maxChampPos = q
                mostPlayedChamp = rankedst['champions'][q]['id']

        mostPlayedChampMatchesCount = float(mostPlayedChampMatchesCount)
        mostPlayedChampKills = rankedst['champions'][maxChampPos]['stats']['totalChampionKills']
        mostPlayedChampDeaths = rankedst['champions'][maxChampPos]['stats']['totalDeathsPerSession']
        mostPlayedChampAssist = rankedst['champions'][maxChampPos]['stats']['totalAssists']
        mostPLayedChampGold = rankedst['champions'][maxChampPos]['stats']['totalGoldEarned'] / mostPlayedChampMatchesCount
        mostPLayedChampGold = round(mostPLayedChampGold, 2)
        mostPlayedChampCs = rankedst['champions'][maxChampPos]['stats']['totalMinionKills'] / mostPlayedChampMatchesCount
        champWinPorcentaje =  rankedst['champions'][maxChampPos]['stats']['totalSessionsWon'] / mostPlayedChampMatchesCount * 100
        champWinPorcentaje = round(champWinPorcentaje, 2)
        mostPlayedChampMatchesWinCount = rankedst['champions'][maxChampPos]['stats']['totalSessionsWon']
        mostPlayedChampMatchesLoseCountPorcentaje = rankedst['champions'][maxChampPos]['stats']['totalSessionsLost'] / mostPlayedChampMatchesCount * 100
        mostPlayedChampMatchesLoseCountPorcentaje = round(mostPlayedChampMatchesLoseCountPorcentaje, 2)
        mostPlayedChampMatchesLoseCount = rankedst['champions'][maxChampPos]['stats']['totalSessionsLost']
        mostPlayedChampMatchesCount = int(mostPlayedChampMatchesCount)

    except(LoLException, KeyError):
        mostPlayedChampKills = 0
        mostPlayedChampDeaths = 0
        mostPlayedChampAssist = 0
        mostPLayedChampGold = 0
        mostPlayedChampCs = 0
        champWinPorcentaje = 0
        mostPlayedChampMatchesWinCount = 0
        mostPlayedChampMatchesLoseCountPorcentaje = 0
        mostPlayedChampMatchesLoseCount = 0
        print ('ERROR')
    mostPlayedChampInfo = {}
    mostPlayedChampInfo['mostPlayedChamp'] = mostPlayedChamp
    mostPlayedChampInfo['mostPlayedChampMatchesCount'] = mostPlayedChampMatchesCount
    mostPlayedChampInfo['mostPlayedChampMatchesWinCount'] = mostPlayedChampMatchesWinCount
    mostPlayedChampInfo['champWinPorcentaje'] = champWinPorcentaje
    mostPlayedChampInfo['mostPlayedChampMatchesLoseCount'] = mostPlayedChampMatchesLoseCount
    mostPlayedChampInfo['mostPlayedChampMatchesLoseCountPorcentaje'] = mostPlayedChampMatchesLoseCountPorcentaje
    mostPlayedChampInfo['mostPlayedChampKills'] = mostPlayedChampKills
    mostPlayedChampInfo['mostPlayedChampAssist'] = mostPlayedChampAssist
    mostPlayedChampInfo['mostPlayedChampDeaths'] = mostPlayedChampDeaths
    mostPlayedChampInfo['mostPLayedChampGold'] = mostPLayedChampGold
    mostPlayedChampInfo['mostPlayedChampCs'] = mostPlayedChampCs
    return mostPlayedChampInfo
    #-->Free Champs
def freeChamps():
    freeChampsRiot = riotWatcher.get_all_free_champions()
    freeChampsId = []
    for j in range(len(freeChampsRiot['champions'])):
        freeChampsId.append(freeChampsRiot['champions'][j]['id'])

    return {'freeChampsId':freeChampsId}

    #-->Partidas
def featuredGames():
    featuredGameType = [0,0,0,0,0]
    champPartida = []
    featuredGames = {}
    featuredGames['partidas'] = [0,0,0,0,0]
    try:
        for k in range(5):
            champFGc = []
            champFGd = []
            featuredGamesRiot = riotWatcher.get_featured_games()
            tiempoSec = featuredGamesRiot['gameList'][k]['gameLength']
            featuredGameType = featuredGamesRiot['gameList'][k]['gameMode']
            for u in range (len(featuredGamesRiot['gameList'][k]['participants'])):
                if featuredGamesRiot['gameList'][k]['participants'][u]['teamId'] == 100 :
                    champFGc.append(featuredGamesRiot['gameList'][k]['participants'][u]['championId'])
                else:
                    champFGd.append(featuredGamesRiot['gameList'][k]['participants'][u]['championId'])
                    
            featuredGames['partidas'][k] = {'featuredGameType':featuredGamesRiot['gameList'][k]['gameMode'] ,'tiempoSec':featuredGamesRiot['gameList'][k]['gameLength'], 'champFGd':champFGd, 'champFGc':champFGc}
    except (LoLException):
        print 'error'

    return featuredGames
    
    #--Historial
def history():
    hpartidasId = 0
    champLvl = 0
    isWin = False
    champId = 0
    gameType = 0
    hmap = 0
    hduracionMin = 0
    hduracionSec = 0
    deaths = 0
    kills = 0
    assists = 0
    goldGained = 0
    creepScore= 0
    piEarned = 0
    createDate = 0
    item1 = 0
    item2 = 0
    item3 = 0
    item4 = 0
    item4 = 0
    item6 = 0
    item7 = 0
    history = {}
    history['partidas'] = [0,0,0,0,0,0,0,0,0,0]

    historial = riotWatcher.get_recent_games(me['id'])
    for o in range (len(historial['games'])):
        champLvl = historial['games'][o]['stats']['level']
        if (historial['games'][o]['stats']['win']):
            isWin = True
        champId = historial['games'][o]['championId']
        gameType = historial['games'][o]['subType']
        hmap = historial['games'][o]['mapId']
        hduracionSec = historial['games'][o]['stats']['timePlayed']
        hduracionMin = historial['games'][o]['stats']['timePlayed'] / 60
        if not 'numDeaths' in historial['games'][o]['stats']:
            deaths = 0
        else:
            deaths = historial['games'][o]['stats']['numDeaths']
        if not 'championsKilled' in historial['games'][o]['stats']:
            kills = 0
        else:
            kills = historial['games'][o]['stats']['championsKilled']
        if not 'assists' in historial['games'][o]['stats']:
            assists = 0
        else:
            assists = historial['games'][o]['stats']['assists']
        goldGained = historial['games'][o]['stats']['goldEarned']
        if not 'minionsKilled' in  historial['games'][o]['stats']:
            creepScore = 0
        else:
            creepScore = historial['games'][o]['stats']['minionsKilled']
        piEarned = historial['games'][o]['ipEarned']
        createDate = historial['games'][o]['createDate'] 
        if not 'item0' in  historial['games'][o]['stats']:
            item1 = 'Vacio'
        else:
            item1 = historial['games'][o]['stats']['item0']
        if not 'item1' in  historial['games'][o]['stats']:
            item2 = 'Vacio'
        else:
            item2 = historial['games'][o]['stats']['item1']
        if not 'item2' in  historial['games'][o]['stats']:
            item3 = 'Vacio'
        else:
            item3 = historial['games'][o]['stats']['item2']
        if not 'item3' in  historial['games'][o]['stats']:
            item4 = 'Vacio'
        else:
            item4 = historial['games'][o]['stats']['item3']
        if not 'item4' in  historial['games'][o]['stats']:
            item5 = 'Vacio'
        else:
            item5 = historial['games'][o]['stats']['item4']
        if not 'item5' in  historial['games'][o]['stats']:
            item6 = 'Vacio'
        else:
            item6 = historial['games'][o]['stats']['item5']
        if not 'item6' in  historial['games'][o]['stats']:
            item7 = 'Vacio'
        else:
            item7 = historial['games'][o]['stats']
        history['partidas'][o] = {'isWin':isWin,'gameType':gameType, 
                                  'hmap':hmap, 'champId':champId, 
                                  'champLvl':champLvl, 'deaths':deaths,
                                  'kills':kills, 'assists':assists, 
                                  'creepScore':creepScore, 'goldGained':goldGained,
                                  'hduracionSec':hduracionSec, 'piEarned':piEarned,
                                  'createDate':createDate, 'item1':item1,
                                  'item6':item6,
                                  'item2':item2,'item3':item3,
                                  'item4':item4,'item5':item5,
                                  'item7':item7
                                 }
    return history


#--Runas
def runes():
    runesWatcher = riotWatcher.get_rune_pages([str(me['id'])])
    runas = {}
    runas['pages'] = []
    pagina = [0,{}]
    
    activaIdRunes = 0
#   try:
    for pag in range (len(runesWatcher[str(me['id'])]['pages'])):
        if (runesWatcher[str(me['id'])]['pages'][pag]['current']):
            activePage = runesWatcher[str(me['id'])]['pages'][pag]['name']
            runas['activePage'] = activePage
        pagina[0] = runesWatcher[str(me['id'])]['pages'][pag]['name']
        for sl in range(len(runesWatcher[str(me['id'])]['pages'][pag]['slots'])):
            if (runesWatcher[str(me['id'])]['pages'][pag]['slots'][sl]['runeId'] not in pagina[1]):
                nom = dataRunes['data'][str(runesWatcher[str(me['id'])]['pages'][pag]['slots'][sl]['runeId'])]['name']
                stats = dataRunes['data'][str(runesWatcher[str(me['id'])]['pages'][pag]['slots'][sl]['runeId'])]['stats'].values()
                pagina[1][str(runesWatcher[str(me['id'])]['pages'][pag]['slots'][sl]['runeId'])] = [nom,1,stats]
            else:
                pagina[1][str(runesWatcher[str(me['id'])]['pages'][pag]['slots'][sl]['runeId'])][1] = pagina[1][str(runesWatcher[str(me['id'])]['pages'][pag]['slots'][sl]['runeId'])][1] + 1
                pagina[1][str(runesWatcher[str(me['id'])]['pages'][pag]['slots'][sl]['runeId'])][2] = pagina[1][str(runesWatcher[str(me['id'])]['pages'][pag]['slots'][sl]['runeId'])][1] * 2
        runas['pages'].append(pagina)
    print runas
            
            
                
                
#    except(KeyError):
#        print 'no runes in page'
    
    return runas
#--Maestrias
def masteries():
    masteries = riotWatcher.get_mastery_pages([str(me['id'])])
    maestrias = {}
    maestrias['pages'] = []
    distribution = [0,0,0]
    activaIdMasteries = 0
    for m in range(len(masteries[str(me['id'])]['pages'])):
        try:
            masteryId = []
            masteryPos = []
            masIdnRank = []
            pagIdMaestries = masteries[str(me['id'])]['pages'][m]['id']
            pagNameMaestries = masteries[str(me['id'])]['pages'][m]['name']
            for mas in range(len(masteries[str(me['id'])]['pages'][m]['masteries'])):
                masteryId.append(masteries[str(me['id'])]['pages'][m]['masteries'][mas]['id'])
                masteryPos.append(masteries[str(me['id'])]['pages'][m]['masteries'][mas]['rank'])
            for idnpos in range(len(masteryId)):
                masIdnRank.append([masteryId[idnpos], masteryPos[idnpos]])
            if masteries[str(me['id'])]['pages'][m]['current']:
                    activaIdMasteries = m
                    for dis in range (len(masteries[str(me['id'])]['pages'][m]['masteries'])):

                        if (masteries[str(me['id'])]['pages'][m]['masteries'][dis]['id'] < 4200):
                            distribution[0] = distribution[0] + masteries[str(me['id'])]['pages'][m]['masteries'][dis]['rank']
                        elif (masteries[str(me['id'])]['pages'][m]['masteries'][dis]['id'] > 4300):
                            distribution[2] = distribution[2] + masteries[str(me['id'])]['pages'][m]['masteries'][dis]['rank']
                        else:
                            distribution[1] = distribution[1] + masteries[str(me['id'])]['pages'][m]['masteries'][dis]['rank']
            maestrias['activePage'] = activaIdMasteries
            maestrias['distribution'] = distribution
            maestrias['pages'].append(pagNameMaestries)
            maestrias['pages'].append(masIdnRank)
        except(KeyError):
            print 'no masteries in page'
    return maestrias


def league():
    ligaWatcher = riotWatcher.get_leaguee([str(me['id'])])
    league = {}
    summonerLeagueTabName = ligaWatcher[str(me['id'])][0]['name']
    summonerLeagueTabRank = ligaWatcher[str(me['id'])][0]['tier']
    league['summonerLeagueTabName'] = summonerLeagueTabName
    league['summonerLeagueTabRank'] = summonerLeagueTabRank
    league['summonerLeagueTabPList'] = []
    league['summonerLeagueTabList'] = []
    for li in range (len(ligaWatcher[str(me['id'])][0]['entries'])):
        try:
            summonerLeagueTabPListName = ligaWatcher[str(me['id'])][0]['entries'][li]['playerOrTeamName']
            summonerLeagueTabPListWins = ligaWatcher[str(me['id'])][0]['entries'][li]['wins']
            summonerLeagueTabPPromo = ligaWatcher[str(me['id'])][0]['entries'][li]['miniSeries']['progress']
            summonerLeagueTabPDivision = ligaWatcher[str(me['id'])][0]['entries'][li]['division']
            summonerLeagueTabPListIsRecent = ligaWatcher[str(me['id'])][0]['entries'][li]['isFreshBlood']
            summonerLeagueTabPListIsOnFire = ligaWatcher[str(me['id'])][0]['entries'][li]['isHotStreak']
            league['summonerLeagueTabPList'].append({'summonerLeagueTabPListName':summonerLeagueTabPListName,
                                                    'summonerLeagueTabPListWins':summonerLeagueTabPListWins,
                                                    'summonerLeagueTabPPromo':summonerLeagueTabPPromo,
                                                    'summonerLeagueTabPDivision':summonerLeagueTabPDivision,
                                                    'summonerLeagueTabPListIsOnFire':summonerLeagueTabPListIsOnFire,
                                                    'summonerLeagueTabPListIsRecent':summonerLeagueTabPListIsRecent
                                                   })
        except(KeyError):
                summonerLeagueTabListName = ligaWatcher[str(me['id'])][0]['entries'][li]['playerOrTeamName']
                summonerLeagueTabListWins = ligaWatcher[str(me['id'])][0]['entries'][li]['wins']
                summonerLeagueTabListIsRecent = ligaWatcher[str(me['id'])][0]['entries'][li]['isFreshBlood']
                summonerLeagueTabListIsOnFire = ligaWatcher[str(me['id'])][0]['entries'][li]['isHotStreak'] 
                summonerLeagueTabListLP = ligaWatcher[str(me['id'])][0]['entries'][li]['leaguePoints']
                summonerLeagueTabDivision = ligaWatcher[str(me['id'])][0]['entries'][li]['division']
                league['summonerLeagueTabList'].append({'summonerLeagueTabListName':summonerLeagueTabListName,
                                                        'summonerLeagueTabListWins':summonerLeagueTabListWins,
                                                        'summonerLeagueTabListIsRecent':summonerLeagueTabListIsRecent,
                                                        'summonerLeagueTabListIsOnFire':summonerLeagueTabListIsOnFire,
                                                        'summonerLeagueTabListLP':summonerLeagueTabListLP,
                                                        'summonerLeagueTabDivision':summonerLeagueTabDivision
                                                       })
            
    return league

def most_common(L):
    return max(g(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]