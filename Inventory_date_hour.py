#!/usr/bin/env python3

"""
 MRF 2017-12-12 - Script para hacer ficheros inventory XML partiendo de las respuestas instrumentales 
                  y complentado la informacion que falta (Lat, Lon, Z, Start_time, End_Time de la
                  Base de datos mysql EDT Array o ficheros de campo.

 MRF 2021-05-14 - Introduzco la posibilidad de pasar la fecha y hora exacta del Inicio y Final estacion
                  hasta el momento se pasaba solo la fecha y la hora inicio se fijaba a las 00:00:00
                  y la de final a las 23:59:59 de los respectivos dias.
                 
                  Nuevo fichero de estaciones: Ex: SANIMS_Sta_Coor_Invetory_TODOnext.csv
                         station;lat;lon;height;install;uninstall
                         C001;42.361828;1.652132;935.77;2021-04-21T22:00:00;2021-06-30T23:59:59
                         C002;42.372780;1.673434;1231.50;2021-04-21T22:00:00;2021-06-30T23:59:59

                  Tendria que funcionar tambien con dias julianos
                         station;lat;lon;height;install;uninstall
                         SF01;42.747172;-8.818683;303.7;2019-155T10:38:54;2019-309T13:31:59
                         SF02;42.741506;-8.850994;142.1;2019-155T18:37:45;2019-277T18:13:59
 MRF 2023-05-22 - He trobat un bug que no se com resoldre be. Si la resposta de la primera estacio de la llista
                  te varies etapes, inventory_utils elimina la segona etapa i es queda amb la primera. Si canvio
                  ordre de lectura i l'estacio de multiples etapes es la segona o qualsevol altre, ho gestiona
                  be i no hi ha problema...


 Documentacion Obspy :

 https://docs.obspy.org/tutorial/code_snippets/stationxml_file_from_scratch.html
 https://docs.obspy.org/packages/obspy.core.inventory.html
 https://docs.obspy.org/packages/autogen/obspy.io.xseed.parser.Parser.html#obspy.io.xseed.parser.Parser

"""

import sys
import os
import glob
import time
import pandas as pd
from obspy.core.inventory import Inventory, Network, Station, Channel, Site
from obspy import read_inventory, UTCDateTime
from obspy.io.xseed import Parser

# Importo una herramientas para limpiar inventarios (inventory_utils.py) - Gener 2018
# https://github.com/SeismicData/pyasdf/blob/master/pyasdf/inventory_utils.py
import inventory_utils

# Cargo el inventario de estaciones para obtener coordenadas, fecha de instalacion y desmantelamineto. 
# Para tener la lista actualizada hay que correr Script: Summary_StaCoor_EDTArray.sh o preparar el fichero
# a mano con las Coordenadas medias delos SOH i las fechas de incicio y fin de los mseed (msi -T).
#
# Manipulamos el fichero resultante como una base de datos Pandas.
#
# Ejemplo de lista inventario: (Hauria de funcionar tambe amb dies Julians)
#
#station;lat;lon;height;install;uninstall
#C001;42.361828;1.652132;935.77;2021-04-21T23:15:00;2021-06-30T22:12:30
#C002;42.372780;1.673434;1231.50;2021-04-22T05:30:00;2021-06-30T11:15:25
#
#station;lat;lon;height;install;uninstall
#SF01;42.747172;-8.818683;303.7;2019-155T10:38:54;2019-309T13:31:59
#SF02;42.741506;-8.850994;142.1;2019-155T18:37:45;2019-277T18:13:59


sta_list=pd.read_csv('YY_Sta_Coor_Inventory_CoorMean_Tot.csv', sep=';', encoding='utf-8')
sta_list=sta_list.T
sta_list.columns = sta_list.iloc[0]
sta_list=sta_list[1:]

# Pedimos varias cosas por el Command Line: El codigo de red a analizar y directorio donde estan las respuestas

print ()
invnetwork = input("  - Introduce the Network code (Ex: YY) :  ")
print (" Network code %s : " % invnetwork)

print ()
direc = input("    - Introduce the response Folder (Ex: ../Response/*) :  ")
print (" Directory containg Responses %s : " % direc)

# Damos nombre al fichero inventory final - Aunque lo defina aqui lo salvo al final de todos los loop    
invfinxml = "%s_Inventory.xml" % (str(invnetwork))
print (" Final Inventroy file name %s : " % invfinxml)

# construyo el path del loop sobre las respuestas:
pathresp = "%s/RESP.%s.*" % (str(direc), str(invnetwork))

print (" Path to Resp files %s : " % pathresp)

# Sampling rate para llenar en el xml en caso de que no venga descrito en la respuesta
# Posible problema respuestas RAU sin firfilters
sps=250
print (" ---- If Sampling Rate is empty, it will be filled by %d !!! ---" % (sps))

print ()
print ("--- 5 Seg to check if everything is correct ---")
time.sleep (5)

# Creamos un inventory vacio al que iremos sumando los inventory generados de lectura de cada respuesta
invfin = Inventory(
    # Las network con sus station y channels se insertan con las respuestas
    networks=[],
    # ID o owner de quien genera el fichero
    source="MRF - GEO3BCN-CSIC")

# Empezamos a leer las respuestas una a una y a rellenar la informacion.
# 
# Al leer la respuesta con Parser y read inventory e ir sumandolo a saco, tenemos muchos campos repetidos
# como por ejemplo la Network que se repite. Se depuran las gerarquias con inventory_utils.py 
# 
for responses in sorted(glob.glob (pathresp)):

# Necesito hacer un fichero intermedio respxml para entrar la respuesta en read_inventory
# no se porque esto no se lo traga: inv = read_inventory (Parser(responses)) ...
  
    respxml = "%s.xml" % (str(responses))
    print (respxml)

    resp = Parser(responses)
    resp.write_xseed (respxml)

# El Inventary es un objeto de 3 pisos/gerarquias ordenadas en: Networks, Stations, Channels
#
# Equivalencias:
#
# net = inv[0] = inv.networks
# sta = net[0] = inv[0][0]
# cha = sta[0] = net[0][0] = inv[0][0][0]

    inv = read_inventory (respxml)

# Borro fichero intermedio - Ya no lo necesito mas
    os.remove (respxml)


    print (" Printing initial Inventory info: ")
    print (inv)

    net = inv[0]

    print (" Filling and Printing Network Info")
    print (" ---------------------------------")
    print (net.code)
    net.description = "XXXXXX project Stations - Y. Lastname - Network %s " % (str(net.code))
    print (net.description)
    print (" ---------------------------------")
    print (net)

# Cuando dentro de la Respuesta hay varias Etapas Start-End (Distintas configuracions de Gain, datalogguer
# o sensor, en el inventory aparecen como distintas Stations y dentro de cada station hay su Channel que 
# habra de rellenar con coordendas y orientaciones.
#
# Busco cuantas etapas/estaciones hay para hacer un loop sobre ellas. Para ello miro cuantas estaciones hay 
# dentro de Network
    num_etapas = len(net)
    print (" This response file has %s Stations" % (str(num_etapas)))

    for i in range (0, num_etapas, 1):

       sta = net[i]


       print (" Filling and Printing Station Info")
       print (" ---------------------------------")
    
       print (sta.code)
       sta.latitude = sta_list [sta.code]['lat']
       print (sta.latitude)
       sta.longitude = sta_list [sta.code]['lon']
       print (sta.longitude)
       sta.elevation = sta_list [sta.code]['height']
       print (sta.elevation)
       print (sta)

# Paso las hora de inicio y fin exactas junto con la fecha de inicio y fin a traves del fichero sta_list.
# Formato de las variables install y uninstall -> 2012-09-07T12:15:00
       sta.start_date = UTCDateTime (sta_list [sta.code]['install'])
       sta.end_date = UTCDateTime (sta_list [sta.code]['uninstall'])


       print (sta.start_date, sta.end_date)
       print (" ---------------------------------")
  
       cha = sta[0]
       print (" Filling and Printing Channel Info")
       print (" ---------------------------------")
       print (cha.code)
       channame = str(cha.code)
       print (channame[2:])
       print (cha.location_code)
       cha.latitude = sta_list [sta.code]['lat']
       print (cha.latitude)
       cha.longitude = sta_list [sta.code]['lon']
       print (cha.longitude)
       cha.elevation = sta_list [sta.code]['height']
       print (cha.elevation)
       cha.depth = 0
       print (cha.depth)

# Intriduzco Azimuth y dip segun canal
       if channame[2:] == "Z":
          cha.dip = -90.0
          cha.azimuth = 0.0

       if channame[2:] == "E":
          cha.dip = 0.0
          cha.azimuth = 90.0

       if channame[2:] == "N":
          cha.dip = 0.0
          cha.azimuth = 0.0

# verificamos si el camp sampling rate esta lleno y sino lo llenamos con el valor fijado en sps
       if cha.sample_rate == 0:
          print ("  -- SAMPLING RATE EMPTY -> FILLING WITH %d sps -- " % (sps))
          cha.sample_rate = sps
       else:
          print ("  -- Sampling Rate OK -- ")

       print (cha.dip)
       print (cha.azimuth)
       print (cha.sample_rate)
       print (cha.start_date, cha.end_date)
       print (cha)
       print (" Printing Response Info")
       print (cha.response)
       print (" --------------------------------------------")


# Saco el plot de la respuesta para verificar
#       respon = cha.response
#       respon.plot(0.001, output="VEL")

# Voy anadiendo las respuestas (ahora inventarios) al inventory final hasta terminar todos los loop
    invfin += inv

# Utilizo las utilidades de inventory_utils.py para eliminar las repeticiones de Estacion y Red
# producto de leer todas las respuestas de todos los canales y estaciones

print (" Cleaning Repetitions - 	Network hierarchy !!")
print (" --------------------------------------------")
inv = invfin
inv_inter = Inventory(networks=[], source='GEO3BCN')
inv = inventory_utils.isolate_and_merge_network(inv, invnetwork)
nets = inv.networks[0]
sta_inv=[nets.stations[i].code for i in range(len(inv.networks[0]))] # lista de estaciones en el inventario
stas=sta_list.columns.tolist() # lista de estaciones en el csv
# 2023-05-22 - Bug - Fins aqui si la resposta de la primera estacio te les multiples etapes hi son. Per algun
#                    motiu a partir d'aqui se les carrega a la primera estacio, pero no a la resta...
for sta in stas:
        if sta in sta_inv:
                inv_inter += inventory_utils.isolate_and_merge_station(inv, invnetwork, sta)
inv_inter = inventory_utils.isolate_and_merge_network(inv_inter, invnetwork)
invfin = inventory_utils.unique_channels(inv_inter)

# Escribo el fichero de inventario final (se pueden hacer kml, css, sacpz, etc)
invfin.write(invfinxml, format='STATIONXML')  

# pinto mapa para ver si estran bien las coordenadas del inventory
invfin.plot ()

print ("End")
print ()
print ()
print ("-------------------------------------------------------------------------------")
print ("Bug 2023/05 --> First Station RespFile CAN NOT have multiple Stages !")
print ("                In that case change the Station Order") 
print ("-------------------------------------------------------------------------------")

