#!/usr/bin/python3

# ----------------------------------------------------------------------------------
#          MRF - Octubre 2024 - Novembre 2025
#
# Script per a tallar, amb el servei fdsnws, dades mseed d'una serie d'estacions
# i guardar-les en un mseed diari amb block size de 512 Bytes per introduir-les
# al playbay del seiscomp via msrtsimul -v -m historic miniSEED_sorted
# abans cal fer un scmssort -u -E miniSEED > miniSEED_sorted - Records are sorted 
# by end time.
#
# https://www.seiscomp.de/doc/base/tutorials/waveformplayback.html#tutorials-rtplayback
# https://docs.obspy.org/packages/obspy.clients.fdsn.html
# Problema: ObsPy can currently not directly read mini-SEED files that are larger 
#           than 2^31 bytes (2048 MiB)
# ----------------------------------------------------------------------------------

import glob
import os
from obspy.core import read
from obspy.clients.fdsn import Client
from obspy import UTCDateTime

# Defineixo el client del que agafare les dades
#
client = Client(base_url='http://geo3bcn-seiscomp.geo3bcn.csic.es:8080/')
#client = Client(base_url='http://eida.geo3bcn.csic.es:8080/')

year = 2025
jul1 = 1
jul2 = 198

# Defineixo el directorio on guardare les dades
#
datapath= "/home/sysop"
outputdir = "Data_playback"

# Definexo Xarxes i Estacions a extreure - Permanents dins de la zona estudi 41.3N-42.6N  1.8E-3.4E
# Totes les loc possibles: 00,res,0K
# Canals BB, SP i Accelerometres
nets="YH,CA,FR,ES,RA"
stations="EP??,SA??,SB??,AVIN,BAIN,BLAN,CBEU,CBRU,CCAS,CELO,CESP,CFON,CGAL,CGAR,CGIR,CGIS,CGRN,CLLI,CORI,CPAL,ICJA,LLIS,MTJR,OLOS,EJON,EXQUE,EXRIP,EXSCF,ZVGAR,SJAF,VALC,PYLL,PYBA,PYPM"
locations= "*"
channels="EH?,HH?,HN?"

# Verifico si existeix el directorio on guardare les dades
#
if os.path.exists ("%s/%s" % (datapath,outputdir)):
  print ("      Directory %s/%s already exists! \n" % (datapath,outputdir))
else:
  os.mkdir("%s/%s" % (datapath,outputdir))
  print ("      Directory %s/%s doesn't exist, we create it now! \n" % (datapath,outputdir))


# Faig el loop extraccio guardant els fitxers mseed finals amb blocks de 512.
# Si tallo fitxers de 24h sobrepassa els 2Gb i Obspy peta, per a fer-ho mes manegable
# faig 2 fitxers per dia: de 00h a 12h i de 12h a 24h.
# Per evitar que faltin dades per problemes fdsnws block size, resto un minut a inici
# i sumo un min al final. 
# En alguns casos aixo dornara pics repetits, pero bueno...
#
# Quedara fer el sort abans del playback amb eines SC: scmssort -u -E
#

k=0 # Contador de fitxers

for jul in range (jul1, jul2 + 1, 1):
    for timei in ["00:00:00.000000","12:00:00.000000"]:

        if timei == "00:00:00.000000":
            timef = "11:59:59.999999"
            filems = "%s/%s/blck512_%d.%03d.00" % (datapath,outputdir,year,jul)
        elif timei == "12:00:00.000000":
            timef = "23:59:59.999999"
            filems = "%s/%s/blck512_%d.%03d.12" % (datapath,outputdir,year,jul)

        k = k + 1  
        tini = "%04d-%03dT%s" % (year, jul, timei)
        tend = "%04d-%03dT%s" % (year, jul, timef)
        starttime = UTCDateTime(tini) - 60
        endtime =  UTCDateTime(tend) + 60

        print ("  Working on File %d - day: %03d/%d  -- > %s -> %s\n" % (k, jul, year, starttime, endtime))
  
        waveform = client.get_waveforms(nets, stations, locations, channels, starttime, endtime)

        print (waveform.__str__(extended=True))

        print ("\n  Output File : %s\n" % (filems))
        waveform.write(str(filems), format='MSEED', reclen=512, encoding='STEIM2')

        waveform.clear()

