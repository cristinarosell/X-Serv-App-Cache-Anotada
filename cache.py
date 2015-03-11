#!/usr/bin/python
# -*- coding: utf-8 -*-


import webapp
import random
import urllib


class Servidor (webapp.webApp):

    # Declare and initialize content
    diccCache = {}

    def parse(self, request):
        url = request.split()[1][1:].split('/')[0]
        cabeceras = request.split('\r\n', 1)[1]
        try:
            peticion = request.split()[1][1:].split('/')[1]
        except IndexError:
            peticion = None

        return (url, cabeceras, peticion)

    def process(self, parsedRequest):
        (url, cabeceras, peticion) = parsedRequest
        url_completa = "http://" + url
        url_inicial = "http://localhost:1234/" + url
        url_orig = "<a href ='" + url_completa + "'> Original </a>"
        url_recargar = "<a href ='" + url_inicial + "'> Recargar </a>"
        petCache = "<a href ='" + url_inicial + "/cache'> Cache </a>"
        cab1 = "<a href ='" + url_inicial + "/cab1'> Cabeceras 1 </a>"
        cab2 = "<a href ='" + url_inicial + "/cab2'> Cabeceras 2 </a>"
        cab3 = "<a href ='" + url_inicial + "/cab3'> Cabeceras 3 </a>"
        cab4 = "<a href ='" + url_inicial + "/cab4'> Cabeceras 4 </a>"

        try:
            f = urllib.urlopen(url_completa)
            html_nuevo = f.read()
        except IOError:
            html_nuevo = ("<html><body>Error</html></body>")
            return ("404 Not Found", html_nuevo)

        urls = ("</br>" + url_orig + "</br>" + url_recargar +
                "</br>" + petCache + "</br>" + cab1 + "</br>" + cab2 +
                "</br>" + cab3 + "</br>" + cab4 + "</br>")

        if peticion == "cab1":
            html_nuevo = ("<html><body>" + "Cabeceras primera iteracion" +
                          cabeceras + urls + "</body></html>")
        elif peticion == "cab2":
            html_nuevo = ("<html><body>" + "Cabeceras segunda iteracion" +
                          cabeceras + urls + "</body></html>")
        elif peticion == "cab3":
            cabeceras3 = f.info()
            html_nuevo = ("<html><body>" + "Cabeceras tercera iteracion" +
                          str(cabeceras3) + urls + "</body></html>")
        elif peticion == "cab4":
            html_nuevo = ("<html><body>" + "Cabeceras cuarta iteracion:" +
                          "no se envian cabeceras al navegador" + urls +
                          "</body></html>")
        elif peticion == "cache":
            try:
                self.diccCache[url] = html_nuevo
            except KeyError:
                html_nuevo = "<html><body>" + Error + urls + "</body></html>"
                return("404 Not Found", html_nuevo)
        else:
            f = urllib.urlopen(url_completa)
            html = f.read()
            princ = html.find('<body')
            fin = html.find('>', princ)
            html_nuevo = (html[:fin+1] + urls + html[(fin+1):])
        return ("200 OK", html_nuevo)


if __name__ == "__main__":
    serv = Servidor("localhost", 1234)
