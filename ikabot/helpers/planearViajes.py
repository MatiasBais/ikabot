#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import math
from decimal import *
from ikabot.helpers.naval import *

def enviarBienes(s, idCiudadOrigen, idCiudadDestino, idIsla, md, vn, mr, cr, az, barcos):
	s.post(payloadPost={'action': 'header', 'function': 'changeCurrentCity', 'actionRequest': s.token(), 'cityId': idCiudadOrigen, 'ajax': '1'}) 
	s.post(payloadPost={'action': 'transportOperations', 'function': 'loadTransportersWithFreight', 'destinationCityId': idCiudadDestino, 'islandId': idIsla, 'oldView': '', 'position': '', 'avatar2Name': '', 'city2Name': '', 'type': '', 'activeTab': '', 'premiumTransporter': '0', 'minusPlusValue': '500', 'cargo_resource': md, 'cargo_tradegood1': vn, 'cargo_tradegood2': mr, 'cargo_tradegood3': cr, 'cargo_tradegood4': az, 'capacity': '5', 'max_capacity': '5', 'jetPropulsion': '0', 'transporters': barcos, 'backgroundView': 'city', 'currentCityId': idCiudadOrigen, 'templateView': 'transport', 'currentTab': 'tabSendTransporter', 'actionRequest': s.token(), 'ajax': '1'})

def planearViajes(s, rutas):
	for ruta in rutas:
		(ciudadOrigen, ciudadDestino, idIsla, md, vn, mr, cr, az) = ruta
		barcosTotales = getBarcosTotales(s)
		while (md + vn + mr + cr + az) > 0:
			barcosDisp = esperarLlegada(s)
			capacidad = barcosDisp * 500
			mdEnv = md if capacidad > md else capacidad
			capacidad -= mdEnv
			md -= mdEnv
			vnEnv = vn if capacidad > vn else capacidad
			capacidad -= vnEnv
			vn -= vnEnv
			mrEnv = mr if capacidad > mr else capacidad
			capacidad -= mrEnv
			mr -= mrEnv
			crEnv = cr if capacidad > cr else capacidad
			capacidad -= crEnv
			cr -= crEnv
			azEnv = az if capacidad > az else capacidad
			capacidad -= azEnv
			az -= azEnv
			cantEnviada = mdEnv + vnEnv + mrEnv + crEnv + azEnv
			barcos = int(math.ceil((Decimal(cantEnviada) / Decimal(500))))
			enviarBienes(s, ciudadOrigen['id'], ciudadDestino['id'], idIsla, mdEnv, vnEnv, mrEnv, crEnv, azEnv, barcos)

def esperarLlegada(s):
	barcos = getBarcosDisponibles(s)
	while barcos == 0:
		html = s.get()
		idCiudad = re.search(r'currentCityId:\s(\d+),', html).group(1)
		url = 'view=militaryAdvisor&oldView=city&oldBackgroundView=city&backgroundView=city&currentCityId={}&actionRequest={}&ajax=1'.format(idCiudad, s.token())
		posted = s.post(url)
		eventos = re.findall(r'"enddate":(\d+),"currentdate":(\d+)}', posted)
		esperaMinima = 10000000
		for evento in eventos:
			tiempoRestante = int(evento[0]) - int(evento[1])
			if tiempoRestante < esperaMinima:
				esperaMinima = tiempoRestante
		if eventos:
			time.sleep(esperaMinima)
		else:
			time.sleep(10 * 60)
		barcos = getBarcosDisponibles(s)
	return barcos
