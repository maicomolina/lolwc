#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Para simular ingreso de muchos usuarios al servidor descomente las lineas terminadas en "#"
import Client
#import time#
#cont = 0#
clientes = []
nosalir = True
cuentas = [
("banersjk","zxmfkmk126"),
("rayder38","caca123"),
("Adriex","adriel1998"),
("Bonzomontreux","bonzomontreux0"),
("Bonzomontreuz","bonzomontreux0"),
("mateosss","Cc:40987366"),
]
try:
    while nosalir:
        #cont+=1#
        #a = cuentas[cont%6][0]#
        #b =cuentas[cont%6][1]#
        #print("con "+str(cont))
        a = raw_input("usuario> ")
        b = raw_input("contraseña> ")
        if a == "send":
            to = raw_input("to> ")
            msg = raw_input("msg> ")
            clientes[b].send(to, msg)
        elif a == "show":
            for i in clientes:
                print(i.jid)
        else:
            cliente = Client.Cliente(a, b, "las")
            if cliente.connected:
                for i in range(len(clientes)):
                    if clientes[i].jid == cliente.jid:
                        clientes.pop(i)
                        break
                clientes.append(cliente)
except KeyboardInterrupt:
    for i in clientes:
        i.close("Cerrando "+str(i.name))
    print("Adios!")
#cliente.send("421651", "Hola como andas?")#Envia Mensaje al summoner con esa id

#cliente.statusMsg = "Mensaje de Estado Nuevo"#modifica una propiedad del cliente
#cliente.refreshStatusFromProps()#Y refresca el estado online con esa nueva propiedad
