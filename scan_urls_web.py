# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import requests
import time

contadorSaltos = 0;

def extraerdatos(url):
    global contadorVisitas
    page = requests.get(url);
    if (page.status_code == 200):   # la página web ha cargado correctamente
        contadorVisitas +=1;
        html = BeautifulSoup(page.content.decode('utf-8', 'ignore'))
        print html.find('title').string + ' visita ' + str(contadorVisitas)
        print html.findAll('a')[2]
        print len(html.findAll('a'))
        time.sleep(1)

extraerdatos('http://miguelms.es')
time.sleep(1)
