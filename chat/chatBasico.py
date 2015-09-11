import xmpp
#se cree un objeto de coneccion con user y pass
#objetos con nombre, estado de coneccion y con historial de chat
conn = xmpp.Client("pvp.net")
server = "la2"
user = "mateosss"
password = "Cc:40987366"

if not conn.connect(server=("chat."+server+".lol.riotgames.com", 5223)):
    print "connect failed."
    exit()

if not conn.auth(user, "AIR_" + password, "xiff"):
    print "auth failed."
    exit()

roster = None

def message_handler(conn, msg):
    user = roster.getName(str(msg.getFrom()))
    text = msg.getBody()

    print "[%s] %s" % (user, text)

    reply = msg.buildReply("[ECHO] %s" % (text))
    reply.setType("chat")
    conn.send(reply)

conn.RegisterHandler("message", message_handler)
conn.sendInitPresence(requestRoster=1)
roster = conn.getRoster()

while conn.isConnected():
    try:
        conn.Process(10)
    except KeyboardInterrupt:
        break
