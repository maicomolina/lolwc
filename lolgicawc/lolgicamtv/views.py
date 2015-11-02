from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

from riotwatcher import LATIN_AMERICA_SOUTH
from riotwatcher import RiotWatcher
from riotwatcher import LoLException

# Create your views here.
''' Aqui esta toda la logica de todos los pedidos a la API de Leage Of Leagends. Por temas de 
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
    sumInf = summonerInfo()
    mpcInf = mostPlayedChampInfo()
    featgames = featuredGames()
    free = freeChamps()
    his = history()
    totalInfo = {}
    runas = runes()
    maestrias = masteries()
    
    # De esta forma los datos ingresan de forma organizada al diccionario con la informacion total
    
    for ii in sumInf:
        totalInfo[ii] = sumInf[ii]
    for jj in mpcInf:
        totalInfo[jj] = mpcInf[jj]
    for oo in featgames:
        totalInfo[oo] = featgames[oo]
    for pp in his:
        totalInfo[pp] = his[pp]
    for cc in free:
        totalInfo[cc] = free[cc]
    for qq in runas:
        totalInfo[qq] = runas[qq]
    for mm in maestrias:
        totalInfo[mm]  = maestrias[mm]
        
    return render_to_response('home.html', totalInfo )
#426174
#-- Informacion del summoner
def summonerInfo():
    try:
        summonerName = me['name']
        #-->Liga
        ligaInfo = riotWatcher.get_league_entry([str(me['id'])])
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
    print "listo"
    print summonerInf
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
    hpartidasId = [0,0,0,0,0,0,0,0,0,0]
    hlevelChamp = [0,0,0,0,0,0,0,0,0,0]
    hwinOrDef = [0,0,0,0,0,0,0,0,0,0]
    hchamp = [0,0,0,0,0,0,0,0,0,0]
    hgameType = [0,0,0,0,0,0,0,0,0,0]
    hmap = [0,0,0,0,0,0,0,0,0,0]
    hduracionMin = [0,0,0,0,0,0,0,0,0,0]
    hduracionSec = [0,0,0,0,0,0,0,0,0,0]
    hdeaths = [0,0,0,0,0,0,0,0,0,0]
    hkills = [0,0,0,0,0,0,0,0,0,0]
    hassists = [0,0,0,0,0,0,0,0,0,0]
    hgoldEarned = [0,0,0,0,0,0,0,0,0,0]
    hminionsKilled = [0,0,0,0,0,0,0,0,0,0]
    hipEarned = [0,0,0,0,0,0,0,0,0,0]
    hdate = [0,0,0,0,0,0,0,0,0,0]
    hitem0 = [0,0,0,0,0,0,0,0,0,0]
    hitem1 = [0,0,0,0,0,0,0,0,0,0]
    hitem2 = [0,0,0,0,0,0,0,0,0,0]
    hitem3 = [0,0,0,0,0,0,0,0,0,0]
    hitem4 = [0,0,0,0,0,0,0,0,0,0]
    hitem5 = [0,0,0,0,0,0,0,0,0,0]
    hitem6 = [0,0,0,0,0,0,0,0,0,0]
    

    historial = riotWatcher.get_recent_games(me['id'])
    for o in range (len(historial['games'])):
        hlevelChamp[o] = historial['games'][o]['stats']['level']
        if (historial['games'][o]['stats']['win']):
            hwinOrDef[o] = 'Victoria'
        else:
            hwinOrDef[o] = 'Derrota'
        hchamp[o] = historial['games'][o]['championId']
        hgameType[o] = historial['games'][o]['subType']
        hmap[o] = historial['games'][o]['mapId']
        hduracionSec[o] = historial['games'][o]['stats']['timePlayed']
        hduracionMin[o] = historial['games'][o]['stats']['timePlayed'] / 60
        if not 'numDeaths' in historial['games'][o]['stats']:
            hdeaths[o] = 0
        else:
            hdeaths[o] = historial['games'][o]['stats']['numDeaths']
        if not 'championsKilled' in historial['games'][o]['stats']:
            hkills[o] = 0
        else:
            hkills[o] = historial['games'][o]['stats']['championsKilled']
        if not 'assists' in historial['games'][o]['stats']:
            hassists[o] = 0
        else:
            hassists[o] = historial['games'][o]['stats']['assists']
        hgoldEarned[o] = historial['games'][o]['stats']['goldEarned']
        if not 'minionsKilled' in  historial['games'][o]['stats']:
            hminionsKilled[o] = 0
        else:
            hminionsKilled[o] = historial['games'][o]['stats']['minionsKilled']
        hipEarned[o] = historial['games'][o]['ipEarned']
        hdate[o] = historial['games'][o]['createDate'] 
        if not 'item0' in  historial['games'][o]['stats']:
            hitem0[o] = 'Vacio'
        else:
            hitem0[o] = historial['games'][o]['stats']['item0']
        if not 'item1' in  historial['games'][o]['stats']:
            hitem1[o] = 'Vacio'
        else:
            hitem1[o] = historial['games'][o]['stats']['item1']
        if not 'item2' in  historial['games'][o]['stats']:
            hitem2[o] = 'Vacio'
        else:
            hitem2[o] = historial['games'][o]['stats']['item2']
        if not 'item3' in  historial['games'][o]['stats']:
            hitem3[o] = 'Vacio'
        else:
            hitem3[o] = historial['games'][o]['stats']['item3']
        if not 'item4' in  historial['games'][o]['stats']:
            hitem4[o] = 'Vacio'
        else:
            hitem4[o] = historial['games'][o]['stats']['item4']
        if not 'item5' in  historial['games'][o]['stats']:
            hitem5[o] = 'Vacio'
        else:
            hitem5[o] = historial['games'][o]['stats']['item5']
        if not 'item6' in  historial['games'][o]['stats']:
            hitem6[o] = 'Vacio'
        else:
            hitem6[o] = historial['games'][o]['stats']
    
        
    return {
                                            'hchamp':hchamp,'hwinOrDef':hwinOrDef,
                                            'hlevelChamp':hlevelChamp ,
                                            'hgameType':hgameType , 'hmap':hmap , 
                                            'hduracionMin':hduracionMin,
                                            'hduracionSec':hduracionSec, 'hdeaths':hdeaths,
                                            'hkills':hkills, 'hassists':hassists,
                                            'hassists':hassists, 'hgoldEarned':hgoldEarned,
                                            'hminionsKilled':hminionsKilled,
                                            'hipEarned':hipEarned,
                                            'hdate':hdate,'hitem0':hitem0,
                                            'hitem1':hitem1,
                                            'hitem2':hitem2,'hitem3':hitem3,
                                            'hitem4':hitem4,'hitem5':hitem5,
                                            'hitem6':hitem6,
                                            }


#--Runas
def runes():
    runes = riotWatcher.get_rune_pages([str(me['id'])])
    runas = {}
    runas['pages'] = []
    activaIdRunes = 0
    for r in range(len(runes[str(me['id'])]['pages'])):
        try:
            runeId = []
            runePos = []
            runIdnPos = []
            pagIdRunes = runes[str(me['id'])]['pages'][r]['id']
            pagNameRunes = runes[str(me['id'])]['pages'][r]['name']
            for sl in range (len(runes[str(me['id'])]['pages'][r]['slots'])):
                runeId.append(runes[str(me['id'])]['pages'][r]['slots'][sl]['runeId'])
                runePos.append(runes[str(me['id'])]['pages'][r]['slots'][sl]['runeSlotId'])
            if runes[str(me['id'])]['pages'][r]['current']:
                activaIdRunes = r
            runas['activePage'] = activaIdRunes
            runas['pages'].append([pagNameRunes])
            for run in range (len(runeId)):
                runIdnPos.append([runeId[run], runePos[run]])
            runas['pages'].append(runIdnPos)  
        except(KeyError):
            print 'no runes in page'
    
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


def most_common(L):
    return max(g(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]