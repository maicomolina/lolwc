#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Client
clientes = []
nosalir = True
try:
    while nosalir:
        a = raw_input("usuario> ")
        b = raw_input("contraseña> ")
        if a == "send":
            to = raw_input("to> ")
            msg = raw_input("msg> ")
            clientes[0].send(to, msg)
        elif a == "show":
            for i in clientes:
                print(i.jid)
        else:
            cliente = Client.Cliente(a, b, "las")
            clientes.append(cliente)
except KeyboardInterrupt:
    for i in clientes:
        i.close()
    print("Adios!")
#cliente.send("421651", "Hola como andas?")#Envia Mensaje al summoner con esa id

#cliente.statusMsg = "Mensaje de Estado Nuevo"#modifica una propiedad del cliente
#cliente.refreshStatusFromProps()#Y refresca el estado online con esa nueva propiedad
