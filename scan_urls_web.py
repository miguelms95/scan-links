# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import requests

contadorSaltos = 0
urlsVisitadas = []
listaUrls = []
MAX_LINKS = 40;                  # Set the max number of links to scan (the net is infinite :P)
URL_SCAN = 'http://google.com'   # Set the page you want to scan

maxEnlaces = 0; # count number of visited
domain = ''

def extraerdatos(url, page_anidada):
    global contadorSaltos, maxEnlaces, domain
    if(domain == ''):
        domain = url.split('/')
        domain = domain [2]
        print domain
    anidacionTabs = ''
    for i in range(page_anidada):
        anidacionTabs = anidacionTabs + '  '
    if (url not in urlsVisitadas) and (domain in url):
        if 'mailto:' in url:
            print anidacionTabs+'error unicode'
        else:
            try:
                page = requests.get(url);
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
                            print anidacionTabs+'#' + str(contadorSaltos) + ' - ' + titulo
                        else:
                            print anidacionTabs+'#' + str(contadorSaltos)
                        urls_pag_raw = html.findAll('a')
                        urls_pag = []
                        for url in urls_pag_raw:
                            url = url.get('href')
                            if(url != None):
                                urls_pag.append(url)
                        anidacionTabs += '\t'
                        for url in urls_pag:
                            if (contadorSaltos <= (MAX_LINKS-1)):
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
            except requests.ConnectionError:
                print anidacionTabs + '!--> connection error'



extraerdatos(URL_SCAN,0)
print '==== STATS ===='
print '' + str(maxEnlaces) + ' links in '+ str(len(urlsVisitadas)) +' page(s)'
