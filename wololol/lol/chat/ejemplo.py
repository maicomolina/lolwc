#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Client
import threading
nosalir = True
def crearCliente(usr, psw):
    cliente = Client.Cliente(usr, psw, "las")

threads = []
while nosalir:
    a = raw_input("usuario> ")
    b = raw_input("contraseña> ")
    threads.append(threading.Thread(target = crearCliente, args = (a,b)))
    threads[len(threads)-1].start()
#cliente.send("421651", "Hola como andas?")#Envia Mensaje al summoner con esa id

#cliente.statusMsg = "Mensaje de Estado Nuevo"#modifica una propiedad del cliente
#cliente.refreshStatusFromProps()#Y refresca el estado online con esa nueva propiedad
