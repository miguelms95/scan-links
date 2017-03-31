# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import requests
import re

contadorSaltos = 0
urlsVisitadas = []
listaUrls = []
MAX_LINKS = 40;
maxEnlaces = 0; # count number of visited

def extraerdatos(url, page_anidada):
    global contadorSaltos, maxEnlaces
    if url not in urlsVisitadas:
        page = requests.get(url);
        anidacionTabs = ''
        for i in range(page_anidada):
            anidacionTabs = anidacionTabs + '\t'
        if (page.status_code == 200):   # la página web ha cargado correctamente
            contadorSaltos +=1;
            urlsVisitadas.append(url)
            try:
                html = BeautifulSoup(page.content.decode('utf-8', 'ignore'))
                titulo = html.find('title')
                if(titulo != None):
                    titulo=titulo.string
                    titulo = str(titulo).replace('\n','')
                    titulo = titulo.replace('\t', ' ')
                    print anidacionTabs+'# ' + str(contadorSaltos) + ' - ' + titulo
                else:
                    print anidacionTabs+'# ' + str(contadorSaltos)
                urls_pag_raw = html.findAll('a')
                urls_pag = []
                for url in urls_pag_raw:
                    url = url.get('href')
                    if(url != None):
                        urls_pag.append(url)
                anidacionTabs += '\t'
                for url in urls_pag:
                    if (maxEnlaces <= MAX_LINKS):
                        url = url.encode('utf-8')
                        if (url != None):  # There are <a> items without 'href' attribute
                            if(url not in listaUrls):
                                if(url != '#' and ('http' or 'https') in url):
                                    print anidacionTabs+'url: ' + str(url)
                                    listaUrls.append(str(url))
                                    maxEnlaces += 1;

                                    extraerdatos(str(url),page_anidada+1)

            except UnicodeEncodeError:
                print anidacionTabs+'error unicode'
        else:
            print anidacionTabs+'! --> Error en la web ' + url +''


extraerdatos('http://miguelms.es',0)
print 'number of different links: ' + str(len(urlsVisitadas))
print contadorSaltos
