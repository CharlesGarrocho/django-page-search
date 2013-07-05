from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.conf import settings
import os
import re

def search(request):
    try:
        busca = request.GET['search']
        busca = busca.encode('utf-8')
    except KeyError:
        busca = None
    pesquisa = []
    conteudo = 'NO'
    argumentos = 'NO'
    quantidade = 'NO'
    if busca is not None:
        argumentos = 'OK'
        if len(busca) > 1:
            quantidade = 'OK'
            regex_busca_str = r'>([^({{)({{%)(}})]*?{0}[^({{)(%}})(}})]*?)<';  # removi >< da primeira parte e <> da segunda parte
            for diretorio in settings.TEMPLATE_DIRS:
                for arquivo in os.listdir(diretorio):
                    with open(diretorio + '/' + arquivo) as arquivo_busca:
                        conteudo_arquivo_busca = arquivo_busca.read()
                        conteudo_arquivo_busca = substitui_constantes_texto(conteudo_arquivo_busca)
                        regex_busca = re.compile(regex_busca_str.format(busca), re.IGNORECASE)
                        resultados_busca = re.search(regex_busca, conteudo_arquivo_busca)
                        if resultados_busca is not None and 'template' not in diretorio:
                            pesquisa.append( {'URL': arquivo.split(".html")[0], 'TEXTO': resultados_busca.groups()[0] })
                            conteudo = 'OK'
    rq = RequestContext(request, {
        'pesquisa': pesquisa,
        'busca': busca,
        'argumentos': argumentos,
        'conteudo': conteudo,
        'quantidade': quantidade
    })
    rq['SITE_NOME'] = settings.SITE_NOME
    return rq


def substitui_constantes_texto(texto):
    if '{{ SITE_NOME }}' in texto:
        texto = texto.replace('{{ SITE_NOME }}', settings.SITE_NOME)
    if '[at]' in texto:
        texto = texto.replace('[at]', '@')
        texto = texto.replace('[dot]', '.')
    #texto = strip_tags(string_value)
    return texto