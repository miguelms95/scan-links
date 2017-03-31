# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import requests

contadorSaltos = 0
urlsVisitadas = []

def extraerdatos(url):
    global contadorSaltos
    if url not in urlsVisitadas:
        page = requests.get(url);
        if (page.status_code == 200):   # la página web ha cargado correctamente
            contadorSaltos +=1;
            html = BeautifulSoup(page.content.decode('utf-8', 'ignore'))
            print ' # ' + str(contadorSaltos) + ' - ' + html.find('title').string
            urls_pagina = html.findAll('a')
            for url in urls_pagina:
                url = url.get('href').encode('utf-8')
                if(url != '#' and ('http' or 'https') in url):
                    print 'url: ' + str(url)
                    urlsVisitadas.append(str(url))
                    extraerdatos(str(url))
        else:
            print 'Error en la web' + url


extraerdatos('http://miguelms.es')
print 'number of links: ' + str(len(urlsVisitadas))
print contadorSaltos
