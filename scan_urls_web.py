# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import requests
import time

contadorSaltos = 0
urlsVisitadas = []

def extraerdatos(url):
    global contadorSaltos
    page = requests.get(url);
    if (page.status_code == 200):   # la página web ha cargado correctamente
        contadorSaltos +=1;
        html = BeautifulSoup(page.content.decode('utf-8', 'ignore'))
        print ' # ' + str(contadorSaltos) + ' - ' + html.find('title').string
        print html.findAll('a')[2]
        urls_pagina = html.findAll('a')

        time.sleep(1)

extraerdatos('http://miguelms.es')
time.sleep(1)

