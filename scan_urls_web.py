# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import requests
import time

contadorSaltos = 0
urlsVisitadas = []
listaUrls = []
enlacesErroneos = 0
listaEnlacesErroneos = []
MAX_LINKS = 500;                  # Set the max number of pages to jump during the scan (the net is infinite :P)
URL_SCAN = 'http://google.com'   # Set the page you want to scan

maxEnlaces = 0; # count number of visited
domain = ''
TRAZA = True

def extraerdatos(url, indentationLevel):
    global contadorSaltos, maxEnlaces, domain, enlacesErroneos, listaEnlacesErroneos
    if(domain == ''):
        if 'http' in url:
            domain = url.split('/')
            domain = domain [2]
            # print domain
    if 'http' not in url:
        url = 'http://'+url

    anidacionTabs = ''
    for i in range(indentationLevel):
        anidacionTabs = anidacionTabs + '  '
    if (url not in urlsVisitadas) and (domain in url): # here comment 'and (domain in url)' for checking the links in the webpages linked too (not recommended)
        if 'mailto:' in url:
            if (TRAZA):
                print anidacionTabs+'ERROR: unicode'
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
                            if(TRAZA):
                                print anidacionTabs+'#' + str(contadorSaltos) + ' - ' + titulo
                        else:
                            if(TRAZA):
                                print anidacionTabs+'#' + str(contadorSaltos)
                        urls_pag_raw = html.findAll('a')
                        urls_pag = []
                        for url in urls_pag_raw:
                            url = url.get('href')
                            if(url != None):
                                urls_pag.append(url)
                        anidacionTabs += ' '
                        for url in urls_pag:
                            if (contadorSaltos <= (MAX_LINKS-1)):
                                url = url.encode('utf-8')
                                if (url != None):  # There are <a> items without 'href' attribute
                                    if(url not in listaUrls):
                                        if(url != '#' and ('http' or 'https') in url):
                                            if(TRAZA):
                                                print anidacionTabs+'Page: ' + str(url)
                                            listaUrls.append(str(url))
                                            maxEnlaces += 1;

                                            extraerdatos(str(url), indentationLevel + 1)

                    except UnicodeEncodeError:
                        if (TRAZA):
                            print anidacionTabs+'error unicode'
                else:
                    enlacesErroneos += 1
                    listaEnlacesErroneos.append(url)
                    if (TRAZA):
                        print anidacionTabs+'## Error loading page: ' + url +''
            except requests.ConnectionError:
                if (TRAZA):
                    print anidacionTabs + '## ERROR: connection error'
            except requests.exceptions.InvalidSchema:
                #print anidacionTabs+ 'Error InvalidSchema'
                return -1

def printStatus():
    print '\n==== STATS ===='
    print '' + str(maxEnlaces) + ' links found in ' + str(len(urlsVisitadas)) + ' page(s)'
    if(enlacesErroneos > 0):
        print '' + str(enlacesErroneos) + ' broken url(s) found:'
        print listaEnlacesErroneos
    else:
        print 'No broken urls found!'

def resetDatos():
    global contadorSaltos, urlsVisitadas, listaEnlacesErroneos, listaUrls, enlacesErroneos, maxEnlaces, domain
    contadorSaltos = 0
    urlsVisitadas = []
    listaUrls = []
    enlacesErroneos = 0
    listaEnlacesErroneos = []
    maxEnlaces = 0;  # count number of visited
    domain = ''

def main():
    global MAX_LINKS, TRAZA
    print 'Welcome to the web URLs Scanner! # Developed by www.miguelms.es'
    print 'Scan all the links in a website. Find broken links!'
    print 'Type \'exit\' to close the program.\n'
    print 'Enter the url to scan with parameters: ' \
          '\n\t\t-nt # Disable the printing trace'# \
          #'\n\t\t-max XX # Set the max number of pages to jump during the scan'
    print 'Example: -> google.com' \
          '\n\t\t-> google.com -nt'
          #'\n\t\t-> google.com -max 100' \
          #'\n\t\t-> google.com -nt -max 100'
    while(1):
        urlToScan = raw_input('-> ')
        if(urlToScan == 'exit'):
            exit(0)
        while '.' not in urlToScan:
            print 'Error: you must enter a valid URL'
            urlToScan = raw_input('-> ')
        '''if '-max' in urlToScan:
            data = urlToScan.split('-max ')
            numberMax = data[1].split(' ')[0]
            print 'numberMax: ' + numberMax
            MAX_LINKS = numberMax
            urlToScan = data[0]
            urlToScan = urlToScan.replace(' ','')
            print 'URL A ESCANEAR: ' + urlToScan'''
        if '-nt' in urlToScan:
            TRAZA = False
            urlToScan = urlToScan.split('-nt')[0]
            urlToScan = urlToScan.replace(' ','')
        start_time = time.time()
        extraerdatos(urlToScan,0)
        finish_time = time.time()
        executionTime = finish_time - start_time
        executionTime = round(executionTime,4)
        print 'Execution time: ' + str(executionTime) + ' s'
        printStatus()
        resetDatos()
        print ''

main()
