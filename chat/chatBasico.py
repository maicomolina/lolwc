#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmpp
import xmltodict
import time
from collections import OrderedDict
#pip install git+https://github.com/ArchipelProject/xmpppy
#se cree un objeto de coneccion con user y pass
#objetos con nombre, estado de coneccion y con historial de chat
conn = xmpp.Client("pvp.net")
server = "la2"
msg = False
#user = "mateosss"
#password = "Cc:40987366"
user = "banersjk"
password = "zxmfkmk126"

statusUser = OrderedDict([(u'body', OrderedDict([(u'profileIcon', u'612'), (u'level', u'30'), (u'wins', u'101'), (u'leaves', u'33'), (u'odinWins', u'0'), (u'odinLeaves', u'0'), (u'queueType', None), (u'rankedLosses', u'0'), (u'rankedRating', u'0'), (u'tier', u'DIAMOND'), (u'rankedSoloRestricted', u'false'), (u'championMasteryScore', u'967'), (u'statusMsg', u'FAFITA 2x1'), (u'rankedLeagueName', u"Tu mama en tanga's league"), (u'rankedLeagueDivision', u'IIIII'), (u'rankedLeagueTier', u'GOLD'), (u'rankedLeagueQueue', u'RANKED_SOLO_5x5'), (u'rankedWins', u'9999'), (u'skinname', u'Riven'), (u'gameQueueType', u'NORMAL'), (u'gameStatus', u'inGame'), (u'timeStamp', u'1442268254517')]))])
statusUserStr = xmltodict.unparse(statusUser)

conectadosJid = []
conectadosRaw = []#Todo en xml de pechaso
conectadosName = []
conectadosChatEstado = []
conectadosEstado = []
conectadosChamp = []
conectadosTiempo = []
conectadosTipoDeCola = []
conectadosChampScore = []
conectadosRankedLeagueQueue = []
conectadosRankedWins = []
conectadosGameQueueType = []
conectadosIcono = []
conectadosMensaje = []
conectadosLevel = []
conectadosLiga = []
conectadosDivision = []
conectadosLigaNombre = []
conectadosVictorias = []
if not conn.connect(server=("chat."+server+".lol.riotgames.com", 5223)):
    print "connect failed."
    exit()

if not conn.auth(user, "AIR_" + password, "xiff"):
    print "auth failed."
    exit()

roster = None

def message_handler(conn, msg):
    print("UKELELELELELELELELELELELEELELELELELELELEELELELELELELELEL")
    print("UKELELELELELELELELELELELEELELELELELELELEELELELELELELELEL")
    print("UKELELELELELELELELELELELEELELELELELELELEELELELELELELELEL")
    print("UKELELELELELELELELELELELEELELELELELELELEELELELELELELELEL")
    print("UKELELELELELELELELELELELEELELELELELELELEELELELELELELELEL")
    
    user = roster.getName(str(msg.getFrom())) 
    text = msg.getBody()

    print "[%s] %s" % (user, text)

    reply = msg.buildReply("[ECHO] %s" % (text))
    reply.setType("chat")
    conn.send(reply)
    print("UKELELELELELELELELELELELEELELELELELELELEELELELELELELELELLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    print("UKELELELELELELELELELELELEELELELELELELELEELELELELELELELEL")
    print("UKELELELELELELELELELELELEELELELELELELELEELELELELELELELEL")

def presence_handler(conn, event):
    jid = event.getFrom().getStripped()
    name = roster.getName(jid)
    status = roster.getStatus(jid)
    chatStatus = roster.getShow(jid)
    if not jid in conectadosJid:
        if status != None:
            conectadosRaw.append(status)
            status = xmltodict.parse(status,encoding='utf-8')
            conectadosJid.append(jid)
            conectadosChatEstado.append(chatStatus)
            conectadosName.append(name)
            if "gameStatus" in status["body"]:
                conectadosEstado.append(status["body"]["gameStatus"])
            else:
                conectadosEstado.append(None)
            if "skinname" in status["body"]:
                conectadosChamp.append(status["body"]["skinname"])
            else:
                conectadosChamp.append(None)
            if "timeStamp" in status["body"]:
                conectadosTiempo.append(status["body"]["timeStamp"])
            else:
                conectadosTiempo.append(None)
            if "queueType" in status["body"]:
                conectadosTipoDeCola.append(status["body"]["queueType"])
            else:
                conectadosTipoDeCola.append(None)
            if "championMasteryScore" in status["body"]:
                conectadosChampScore.append(status["body"]["championMasteryScore"])
            else:
                conectadosChampScore.append(None)
            if "rankedLeagueQueue" in status["body"]:
                conectadosRankedLeagueQueue.append(status["body"]["rankedLeagueQueue"])
            else:
                conectadosRankedLeagueQueue.append(None)
            if "rankedWins" in status["body"]:
                conectadosRankedWins.append(status["body"]["rankedWins"])
            else:
                conectadosRankedWins.append(None)
            if "gameQueueType" in status["body"]:
                conectadosGameQueueType.append(status["body"]["gameQueueType"])
            else:
                conectadosGameQueueType.append(None)
            if "profileIcon" in status["body"]:
                conectadosIcono.append(status["body"]["profileIcon"])
            else:
                conectadosIcono.append(None)
            if "statusMsg" in status["body"]:
                conectadosMensaje.append(status["body"]["statusMsg"])
            else:
                conectadosMensaje.append(None)
            if "level" in status["body"]:
                conectadosLevel.append(status["body"]["level"])
            else:
                conectadosLevel.append(None)
            if "rankedLeagueTier" in status["body"]:
                conectadosLiga.append(status["body"]["rankedLeagueTier"])
            else:
                conectadosLiga.append(None)
            if "rankedLeagueDivision" in status["body"]:
                conectadosDivision.append(status["body"]["rankedLeagueDivision"])
            else:
                conectadosDivision.append(None)
            if "rankedLeagueName" in status["body"]:
                conectadosLigaNombre.append(status["body"]["rankedLeagueName"])
            else:
                conectadosLigaNombre.append(None)
            if "wins" in status["body"]:
                conectadosVictorias.append(status["body"]["wins"])
            else:
                conectadosVictorias.append(None)
        
roster = conn.getRoster()
conn.RegisterHandler("message", message_handler)
conn.RegisterHandler("presence", presence_handler)
pres = xmpp.Presence()
pres.setStatus(statusUserStr)
conn.send(pres)
#conn.sendInitPresence(requestRoster=1)


while conn.isConnected():
    try:
        conn.Process(10)
        print("------------------------")
        for i in range(len(conectadosJid)):
            print("\tJid: "+str(conectadosJid[i]))
            print("\tSummoner: "+str(conectadosName[i]))
            print("\tEstado de Chat: "+str(conectadosChatEstado[i]))
            print("\tEstado: "+str(conectadosEstado[i]))
            print("\tJugando: "+str(conectadosChamp[i]))
            print("\tTipo de Cola: "+str(conectadosTipoDeCola[i]))
            print("\tChamp Score: "+str(conectadosChampScore[i]))
            print("\tRanked League Queue: "+str(conectadosRankedLeagueQueue[i]))
            print("\tVictorias en Ranked: "+str(conectadosRankedWins[i]))
            print("\tGame Queue Type: "+str(conectadosGameQueueType[i]))
            if conectadosTiempo[i]:
                minutos = str((time.time() - float(conectadosTiempo[i][0:10]+"."+conectadosTiempo[i][10:13]))/60)+" minutos"
            else:
                minutos = "---"
            
            print("\tDurante: "+ minutos + " > " + str(conectadosTiempo[i]))
            print("\tIcono: "+str(conectadosIcono[i]))
            print("\tMensaje: "+str(conectadosMensaje[i]))
            print("\tLevel: "+str(conectadosLevel[i]))
            print("\tLiga: "+str(conectadosLiga[i]))
            print("\tDivision: "+str(conectadosDivision[i]))
            print("\tNombre de Liga: "+str(conectadosLigaNombre[i]))
            print("\tVictorias: "+str(conectadosVictorias[i]))
            print("")
        print("------------------------")
    except KeyboardInterrupt:
        break
