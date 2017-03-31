# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import requests

contadorSaltos = 0
urlsVisitadas = []
listaUrls = []
MAX_LINKS = 5;
maxEnlaces = 0; # count number of visited

def extraerdatos(url):
    global contadorSaltos, maxEnlaces
    if url not in urlsVisitadas:
        page = requests.get(url);
        if (page.status_code == 200):   # la página web ha cargado correctamente
            contadorSaltos +=1;
            urlsVisitadas.append(url)
            try:
                html = BeautifulSoup(page.content.decode('utf-8', 'ignore'))
                titulo = html.find('title')
                if(titulo != None):
                    titulo=titulo.string
                    print ' # ' + str(contadorSaltos) + ' - ' + titulo
                else:
                    print ' # ' + str(contadorSaltos)
                urls_pag_raw = html.findAll('a')
                urls_pag = []
                for url in urls_pag_raw:
                    url = url.get('href')
                    if(url != None):
                        urls_pag.append(url)
                for url in urls_pag:
                    if (maxEnlaces <= MAX_LINKS):
                        url = url.encode('utf-8')
                        if (url != None):  # There are <a> items without 'href' attribute
                            if(url not in listaUrls):
                                if(url != '#' and ('http' or 'https') in url):
                                    print 'url: ' + str(url)
                                    listaUrls.append(str(url))
                                    maxEnlaces += 1;
                                    extraerdatos(str(url))
            except UnicodeEncodeError:
                print 'error unicode'
        else:
            print '! --> Error en la web ' + url +'\n'


extraerdatos('http://miguelms.es')
print 'number of different links: ' + str(len(urlsVisitadas))
print contadorSaltos
