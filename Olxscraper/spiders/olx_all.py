# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
import useragent
from Olxscraper.items import OlxscraperItem
from scrapy.http import Request, FormRequest
from copy import deepcopy
from time import sleep
import time
import re
import random
import base64
import datetime
import csv
import json

categs = [
    "animais-e-acessorios",
    "bebes-e-criancas",
    "musica-e-hobbies",
    "moda-e-beleza",
    "para-a-sua-casa",
    "esportes",
    "eletronicos-e-celulares",
    "veiculos",
    "empregos-e-negocios",
    "imoveis",
]

urls = [
    'http://sp.olx.com.br/sao-paulo-e-regiao?f=p',
    'http://sp.olx.com.br/grande-campinas?f=p',
    'http://sp.olx.com.br/vale-do-paraiba-e-litoral-norte?f=p',
    'http://sp.olx.com.br/regiao-de-sorocaba?f=p',
    'http://sp.olx.com.br/baixada-santista-e-litoral-sul?f=p',
    'http://sp.olx.com.br/regiao-de-ribeirao-preto?f=p',
    'http://sp.olx.com.br/regiao-de-sao-jose-do-rio-preto?f=p',
    'http://sp.olx.com.br/regiao-de-bauru-e-marilia?f=p',
    'http://sp.olx.com.br/regiao-de-presidente-prudente?f=p',
    'http://rj.olx.com.br/rio-de-janeiro-e-regiao?f=p',
    'http://rj.olx.com.br/norte-do-estado-do-rio?f=p',
    'http://rj.olx.com.br/serra-angra-dos-reis-e-regiao?f=p',
    'http://mg.olx.com.br/belo-horizonte-e-regiao?f=p',
    'http://mg.olx.com.br/regiao-de-uberlandia-e-uberaba?f=p',
    'http://mg.olx.com.br/regiao-de-juiz-de-fora?f=p',
    'http://mg.olx.com.br/regiao-de-pocos-de-caldas-e-varginha?f=p',
    'http://mg.olx.com.br/regiao-de-montes-claros-e-diamantina?f=p',
    'http://mg.olx.com.br/regiao-de-governador-valadares-e-teofilo-otoni?f=p',
    'http://mg.olx.com.br/regiao-de-divinopolis?f=p',
    'http://pr.olx.com.br/regiao-de-curitiba-e-paranagua?f=p',
    'http://pr.olx.com.br/regiao-de-londrina?f=p',
    'http://pr.olx.com.br/regiao-de-maringa?f=p',
    'http://pr.olx.com.br/regiao-de-foz-do-iguacu-e-cascavel?f=p',
    'http://pr.olx.com.br/regiao-de-ponta-grossa-e-guarapuava?f=p',
    'http://pr.olx.com.br/regiao-de-francisco-beltrao-e-pato-branco?f=p',
    'http://ba.olx.com.br/grande-salvador?f=p',
    'http://ba.olx.com.br/regiao-de-feira-de-santana-e-alagoinhas?f=p',
    'http://ba.olx.com.br/sul-da-bahia?f=p',
    'http://ba.olx.com.br/regiao-de-vitoria-da-conquista-e-barreiras?f=p',
    'http://ba.olx.com.br/regiao-de-juazeiro-e-jacobina?f=p',
    'http://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul?f=p',
    'http://rs.olx.com.br/regioes-de-caxias-do-sul-e-passo-fundo?f=p',
    'http://rs.olx.com.br/regioes-de-pelotas-rio-grande-e-bage?f=p',
    'http://rs.olx.com.br/regioes-de-santa-maria-uruguaiana-e-cruz-alta?f=p',
    'http://go.olx.com.br/grande-goiania-e-anapolis?f=p',
    'http://go.olx.com.br/regiao-de-rio-verde-e-caldas-novas?f=p',
    'http://pe.olx.com.br/grande-recife?f=p',
    'http://pe.olx.com.br/regiao-de-petrolina-e-garanhuns?f=p',
    'http://am.olx.com.br/regiao-de-manaus?f=p',
    'http://am.olx.com.br/leste-do-amazonas?f=p',
    'http://ce.olx.com.br/fortaleza-e-regiao?f=p',
    'http://ce.olx.com.br/regiao-de-juazeiro-do-norte-e-sobral?f=p',
    'http://pa.olx.com.br/regiao-de-belem?f=p',
    'http://pa.olx.com.br/regiao-de-santarem?f=p',
    'http://pa.olx.com.br/regiao-de-maraba?f=p',
    'http://sc.olx.com.br/florianopolis-e-regiao?f=p',
    'http://sc.olx.com.br/norte-de-santa-catarina?f=p',
    'http://sc.olx.com.br/oeste-de-santa-catarina?f=p',
    'http://df.olx.com.br/distrito-federal-e-regiao/brasilia?f=p',
    'http://df.olx.com.br/distrito-federal-e-regiao/outras-cidades?f=p',
    'http://es.olx.com.br/norte-do-espirito-santo?f=p',
    'http://es.olx.com.br/sul-do-espirito-santo?f=p',
    'http://pb.olx.com.br/paraiba/joao-pessoa?f=p',
    'http://pb.olx.com.br/paraiba/campina-grande-guarabira-e-regiao?f=p',
    'http://pb.olx.com.br/paraiba/santa-rita-bayeux-e-regiao?f=p',
    'http://pb.olx.com.br/paraiba/patos-sousa-e-regiao?f=p',
    'http://pb.olx.com.br/paraiba/monteiro-picui-e-regiao?f=p',
    'http://se.olx.com.br/?f=p',
    'http://ma.olx.com.br/regiao-de-sao-luis?f=p',
    'http://ma.olx.com.br/regiao-de-imperatriz-e-caxias?f=p',
    'http://rn.olx.com.br/?f=p',
    'http://ms.olx.com.br/mato-grosso-do-sul/campo-grande?f=p',
    'http://ms.olx.com.br/mato-grosso-do-sul/dourados?f=p',
    'http://ms.olx.com.br/mato-grosso-do-sul/tres-lagoas?f=p',
    'http://ms.olx.com.br/mato-grosso-do-sul/corumba?f=p',
    'http://ms.olx.com.br/mato-grosso-do-sul/outras-cidades?f=p',
    'http://al.olx.com.br/?f=p',
    'http://ro.olx.com.br/?f=p',
    'http://mt.olx.com.br/regiao-de-cuiaba?f=p',
    'http://mt.olx.com.br/regiao-de-rondonopolis-e-sinop?f=p',
    'http://rr.olx.com.br/?f=p',
    'http://pi.olx.com.br/regiao-de-teresina-e-parnaiba?f=p',
    'http://pi.olx.com.br/regiao-de-picos-e-floriano?f=p',
    'http://ap.olx.com.br/?f=p',
    'http://ac.olx.com.br/?f=p',
    'http://to.olx.com.br/?f=p',
    'http://sp.olx.com.br/sao-paulo-e-regiao?f=c',
    'http://sp.olx.com.br/grande-campinas?f=c',
    'http://sp.olx.com.br/vale-do-paraiba-e-litoral-norte?f=c',
    'http://sp.olx.com.br/regiao-de-sorocaba?f=c',
    'http://sp.olx.com.br/baixada-santista-e-litoral-sul?f=c',
    'http://sp.olx.com.br/regiao-de-ribeirao-preto?f=c',
    'http://sp.olx.com.br/regiao-de-sao-jose-do-rio-preto?f=c',
    'http://sp.olx.com.br/regiao-de-bauru-e-marilia?f=c',
    'http://sp.olx.com.br/regiao-de-presidente-prudente?f=c',
    'http://rj.olx.com.br/rio-de-janeiro-e-regiao?f=c',
    'http://rj.olx.com.br/norte-do-estado-do-rio?f=c',
    'http://rj.olx.com.br/serra-angra-dos-reis-e-regiao?f=c',
    'http://mg.olx.com.br/belo-horizonte-e-regiao?f=c',
    'http://mg.olx.com.br/regiao-de-uberlandia-e-uberaba?f=c',
    'http://mg.olx.com.br/regiao-de-juiz-de-fora?f=c',
    'http://mg.olx.com.br/regiao-de-pocos-de-caldas-e-varginha?f=c',
    'http://mg.olx.com.br/regiao-de-montes-claros-e-diamantina?f=c',
    'http://mg.olx.com.br/regiao-de-governador-valadares-e-teofilo-otoni?f=c',
    'http://mg.olx.com.br/regiao-de-divinopolis?f=c',
    'http://pr.olx.com.br/regiao-de-curitiba-e-paranagua?f=c',
    'http://pr.olx.com.br/regiao-de-londrina?f=c',
    'http://pr.olx.com.br/regiao-de-maringa?f=c',
    'http://pr.olx.com.br/regiao-de-foz-do-iguacu-e-cascavel?f=c',
    'http://pr.olx.com.br/regiao-de-ponta-grossa-e-guarapuava?f=c',
    'http://pr.olx.com.br/regiao-de-francisco-beltrao-e-pato-branco?f=c',
    'http://ba.olx.com.br/grande-salvador?f=c',
    'http://ba.olx.com.br/regiao-de-feira-de-santana-e-alagoinhas?f=c',
    'http://ba.olx.com.br/sul-da-bahia?f=c',
    'http://ba.olx.com.br/regiao-de-vitoria-da-conquista-e-barreiras?f=c',
    'http://ba.olx.com.br/regiao-de-juazeiro-e-jacobina?f=c',
    'http://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul?f=c',
    'http://rs.olx.com.br/regioes-de-caxias-do-sul-e-passo-fundo?f=c',
    'http://rs.olx.com.br/regioes-de-pelotas-rio-grande-e-bage?f=c',
    'http://rs.olx.com.br/regioes-de-santa-maria-uruguaiana-e-cruz-alta?f=c',
    'http://go.olx.com.br/grande-goiania-e-anapolis?f=c',
    'http://go.olx.com.br/regiao-de-rio-verde-e-caldas-novas?f=c',
    'http://pe.olx.com.br/grande-recife?f=c',
    'http://pe.olx.com.br/regiao-de-petrolina-e-garanhuns?f=c',
    'http://am.olx.com.br/regiao-de-manaus?f=c',
    'http://am.olx.com.br/leste-do-amazonas?f=c',
    'http://ce.olx.com.br/fortaleza-e-regiao?f=c',
    'http://ce.olx.com.br/regiao-de-juazeiro-do-norte-e-sobral?f=c',
    'http://pa.olx.com.br/regiao-de-belem?f=c',
    'http://pa.olx.com.br/regiao-de-santarem?f=c',
    'http://pa.olx.com.br/regiao-de-maraba?f=c',
    'http://sc.olx.com.br/florianopolis-e-regiao?f=c',
    'http://sc.olx.com.br/norte-de-santa-catarina?f=c',
    'http://sc.olx.com.br/oeste-de-santa-catarina?f=c',
    'http://df.olx.com.br/distrito-federal-e-regiao/brasilia?f=c',
    'http://df.olx.com.br/distrito-federal-e-regiao/outras-cidades?f=c',
    'http://es.olx.com.br/norte-do-espirito-santo?f=c',
    'http://es.olx.com.br/sul-do-espirito-santo?f=c',
    'http://pb.olx.com.br/paraiba/joao-pessoa?f=c',
    'http://pb.olx.com.br/paraiba/campina-grande-guarabira-e-regiao?f=c',
    'http://pb.olx.com.br/paraiba/santa-rita-bayeux-e-regiao?f=c',
    'http://pb.olx.com.br/paraiba/patos-sousa-e-regiao?f=c',
    'http://pb.olx.com.br/paraiba/monteiro-picui-e-regiao?f=c',
    'http://se.olx.com.br/?f=c',
    'http://ma.olx.com.br/regiao-de-sao-luis?f=c',
    'http://ma.olx.com.br/regiao-de-imperatriz-e-caxias?f=c',
    'http://rn.olx.com.br/?f=c',
    'http://ms.olx.com.br/mato-grosso-do-sul/campo-grande?f=c',
    'http://ms.olx.com.br/mato-grosso-do-sul/dourados?f=c',
    'http://ms.olx.com.br/mato-grosso-do-sul/tres-lagoas?f=c',
    'http://ms.olx.com.br/mato-grosso-do-sul/corumba?f=c',
    'http://ms.olx.com.br/mato-grosso-do-sul/outras-cidades?f=c',
    'http://al.olx.com.br/?f=c',
    'http://ro.olx.com.br/?f=c',
    'http://mt.olx.com.br/regiao-de-cuiaba?f=c',
    'http://mt.olx.com.br/regiao-de-rondonopolis-e-sinop?f=c',
    'http://rr.olx.com.br/?f=c',
    'http://pi.olx.com.br/regiao-de-teresina-e-parnaiba?f=c',
    'http://pi.olx.com.br/regiao-de-picos-e-floriano?f=c',
    'http://ap.olx.com.br/?f=c',
    'http://ac.olx.com.br/?f=c',
    'http://to.olx.com.br/?f=c',

    #'Sequence of Crawling for Professionl  Ads',

    'http://sp.olx.com.br/sao-paulo-e-regiao?f=c',
    'http://sp.olx.com.br/grande-campinas?f=c',
    'http://sp.olx.com.br/vale-do-paraiba-e-litoral-norte?f=c',
    'http://sp.olx.com.br/regiao-de-sorocaba?f=c',
    'http://sp.olx.com.br/baixada-santista-e-litoral-sul?f=c',
    'http://sp.olx.com.br/regiao-de-ribeirao-preto?f=c',
    'http://sp.olx.com.br/regiao-de-sao-jose-do-rio-preto?f=c',
    'http://sp.olx.com.br/regiao-de-bauru-e-marilia?f=c',
    'http://sp.olx.com.br/regiao-de-presidente-prudente?f=c',
    'http://rj.olx.com.br/rio-de-janeiro-e-regiao?f=c',
    'http://rj.olx.com.br/norte-do-estado-do-rio?f=c',
    'http://rj.olx.com.br/serra-angra-dos-reis-e-regiao?f=c',
    'http://mg.olx.com.br/belo-horizonte-e-regiao?f=c',
    'http://mg.olx.com.br/regiao-de-uberlandia-e-uberaba?f=c',
    'http://mg.olx.com.br/regiao-de-juiz-de-fora?f=c',
    'http://mg.olx.com.br/regiao-de-pocos-de-caldas-e-varginha?f=c',
    'http://mg.olx.com.br/regiao-de-montes-claros-e-diamantina?f=c',
    'http://mg.olx.com.br/regiao-de-governador-valadares-e-teofilo-otoni?f=c',
    'http://mg.olx.com.br/regiao-de-divinopolis?f=c',
    'http://pr.olx.com.br/regiao-de-curitiba-e-paranagua?f=c',
    'http://pr.olx.com.br/regiao-de-londrina?f=c',
    'http://pr.olx.com.br/regiao-de-maringa?f=c',
    'http://pr.olx.com.br/regiao-de-foz-do-iguacu-e-cascavel?f=c',
    'http://pr.olx.com.br/regiao-de-ponta-grossa-e-guarapuava?f=c',
    'http://pr.olx.com.br/regiao-de-francisco-beltrao-e-pato-branco?f=c',
    'http://ba.olx.com.br/grande-salvador?f=c',
    'http://ba.olx.com.br/regiao-de-feira-de-santana-e-alagoinhas?f=c',
    'http://ba.olx.com.br/sul-da-bahia?f=c',
    'http://ba.olx.com.br/regiao-de-vitoria-da-conquista-e-barreiras?f=c',
    'http://ba.olx.com.br/regiao-de-juazeiro-e-jacobina?f=c',
    'http://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul?f=c',
    'http://rs.olx.com.br/regioes-de-caxias-do-sul-e-passo-fundo?f=c',
    'http://rs.olx.com.br/regioes-de-pelotas-rio-grande-e-bage?f=c',
    'http://rs.olx.com.br/regioes-de-santa-maria-uruguaiana-e-cruz-alta?f=c',
    'http://go.olx.com.br/grande-goiania-e-anapolis?f=c',
    'http://go.olx.com.br/regiao-de-rio-verde-e-caldas-novas?f=c',
    'http://pe.olx.com.br/grande-recife?f=c',
    'http://pe.olx.com.br/regiao-de-petrolina-e-garanhuns?f=c',
    'http://am.olx.com.br/regiao-de-manaus?f=c',
    'http://am.olx.com.br/leste-do-amazonas?f=c',
    'http://ce.olx.com.br/fortaleza-e-regiao?f=c',
    'http://ce.olx.com.br/regiao-de-juazeiro-do-norte-e-sobral?f=c',
    'http://pa.olx.com.br/regiao-de-belem?f=c',
    'http://pa.olx.com.br/regiao-de-santarem?f=c',
    'http://pa.olx.com.br/regiao-de-maraba?f=c',
    'http://sc.olx.com.br/florianopolis-e-regiao?f=c',
    'http://sc.olx.com.br/norte-de-santa-catarina?f=c',
    'http://sc.olx.com.br/oeste-de-santa-catarina?f=c',
    'http://df.olx.com.br/distrito-federal-e-regiao/brasilia?f=c',
    'http://df.olx.com.br/distrito-federal-e-regiao/outras-cidades?f=c',
    'http://es.olx.com.br/norte-do-espirito-santo?f=c',
    'http://es.olx.com.br/sul-do-espirito-santo?f=c',
    'http://pb.olx.com.br/paraiba/joao-pessoa?f=c',
    'http://pb.olx.com.br/paraiba/campina-grande-guarabira-e-regiao?f=c',
    'http://pb.olx.com.br/paraiba/santa-rita-bayeux-e-regiao?f=c',
    'http://pb.olx.com.br/paraiba/patos-sousa-e-regiao?f=c',
    'http://pb.olx.com.br/paraiba/monteiro-picui-e-regiao?f=c',
    'http://se.olx.com.br/?f=c',
    'http://ma.olx.com.br/regiao-de-sao-luis?f=c',
    'http://ma.olx.com.br/regiao-de-imperatriz-e-caxias?f=c',
    'http://rn.olx.com.br/?f=c',
    'http://ms.olx.com.br/mato-grosso-do-sul/campo-grande?f=c',
    'http://ms.olx.com.br/mato-grosso-do-sul/dourados?f=c',
    'http://ms.olx.com.br/mato-grosso-do-sul/tres-lagoas?f=c',
    'http://ms.olx.com.br/mato-grosso-do-sul/corumba?f=c',
    'http://ms.olx.com.br/mato-grosso-do-sul/outras-cidades?f=c',
    'http://al.olx.com.br/?f=c',
    'http://ro.olx.com.br/?f=c',
    'http://mt.olx.com.br/regiao-de-cuiaba?f=c',
    'http://mt.olx.com.br/regiao-de-rondonopolis-e-sinop?f=c',
    'http://rr.olx.com.br/?f=c',
    'http://pi.olx.com.br/regiao-de-teresina-e-parnaiba?f=c',
    'http://pi.olx.com.br/regiao-de-picos-e-floriano?f=c',
    'http://ap.olx.com.br/?f=c',
    'http://ac.olx.com.br/?f=c',
    'http://to.olx.com.br/?f=c']

all_urls = []

for url in urls:
    sp = url.split("?")
    for cat in categs:
        f_url = sp[0] + "/" + cat + "?" + sp[1] + " " + cat
        all_urls.append(f_url)


class OlxspiderSpider(scrapy.Spider):
    name = "olx_all"
    allowed_domains = ["olx.com"]
    start_urls = (
        'http://www.olx.com.br/brasil',
    )

    categories = {
        "/veiculos/carros veiculos",
        "/veiculos/pecas-e-acessorios veiculos",
        "/veiculos/motos veiculos",
        "/veiculos/caminhoes-onibus-e-vans veiculos",
        "/veiculos/barcos-lanchas-e-avioes veiculos",
        "/servicos empregos-e-negocios",
        "/industria-comercio-e-agro empregos-e-negocios",
        "/ofertas-de-emprego empregos-e-negocios",
        "/procuro-emprego empregos-e-negocios",
        "/imoveis/venda imoveis",
        "/imoveis/aluguel imoveis",
        "/imoveis/lojas-salas-e-outros imoveis",
        "/imoveis/terrenos imoveis",
        "/imoveis/temporada imoveis",
        "/imoveis/lancamentos imoveis",
        "/celulares eletronicos-e-celulares",
        "/computadores-e-acessorios eletronicos-e-celulares",
        "/audio-tv-video-e-fotografia eletronicos-e-celulares",
        "/videogames eletronicos-e-celulares",
        "/esportes-e-ginastica esportes",
        "/ciclismo esportes",
        "/moveis para-a-sua-casa",
        "/eletrodomesticos para-a-sua-casa",
        "/arte-e-decoracao para-a-sua-casa",
        "/jardinagem-e-construcao para-a-sua-casa",
        "/cama-mesa-e-banho para-a-sua-casa",
        "/roupas-e-calcados moda-e-beleza",
        "/bijouteria-relogios-e-acessorios moda-e-beleza",
        "/beleza-e-saude moda-e-beleza",
        "/bolsas-malas-e-mochilas moda-e-beleza",
        "/instrumentos-musicais musica-e-hobbies",
        "/livros-e-revistas musica-e-hobbies",
        "/hobbies-e-colecoes musica-e-hobbies",
        "/musica-e-filmes musica-e-hobbies",
        "/antiguidades musica-e-hobbies",
        "/bebes-e-criancas bebes-e-criancas",
        "/animais-e-acessorios/cachorros cachorros",
        "/animais-e-acessorios/outros-animais outros-animais",
        "/animais-e-acessorios/artigos-para-peixes artigos-para-peixes",
        "/animais-e-acessorios/cavalos cavalos",
        "/animais-e-acessorios/gatos gatos",
        "/animais-e-acessorios/roedores roedores"
    }

    useragent_lists = useragent.user_agent_list
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': useragent_lists[random.randrange(0, len(useragent_lists))],
    }

    def start_requests(self):
        index = len(all_urls)
        for u in all_urls:
            url = u.split(" ")[0]
            main_cate = u.split(" ")[1]
            req = scrapy.Request(url=url, headers=self.headers,
                                 callback=self.getDataUrl, dont_filter=True,
                                  meta={'priority': index}
                                 )
            req.meta['main_cate'] = main_cate
            index = index -1
            yield req

    def getMain(self, response):
        print "========== Start =========="

        countries = response.xpath(
            '//div[@class="linkshelf-tabs-content country"]/ul[@class="list"]/li[@class="item"]')
        # print len(countries)
        for cnt, country in enumerate(countries):
            # test
            # if cnt>1:
            #     return
            itemUrl = country.xpath('p/a/@href').extract()[0]

            req = scrapy.Request(
                url=itemUrl, headers=self.headers, callback=self.getStateUrl, dont_filter=True)
            # print "------ country -------"
            # print itemUrl
            req.meta['countryUrl'] = itemUrl

            yield req

    def getStateUrl(self, response):
        print "========= Get State Urls ========="
        countryUrl = response.meta['countryUrl']

        states = response.xpath(
            '//div[@class="linkshelf-tabs-content state"]/ul[@class="list"]/li[@class="item"]')
        # print len(states)
        if len(states):
            for state in states:
                itemUrl = state.xpath('p/a/@href').extract()[0]
                # print "------ state -------"
                # print itemUrl
                req = scrapy.Request(
                    url=itemUrl, headers=self.headers, callback=self.getZoneUrl, dont_filter=True)
                yield req
                # return

        else:
            zones = response.xpath(
                '//div[@class="linkshelf-tabs-content zones"]//a[@class="link"]')
            # print len(zones)
            if len(zones):
                for zone in zones:
                    # print "--------- zone --------"
                    itemUrl = zone.xpath('@href').extract()[0]

                    # print itemUrl
                    for category in self.categories:
                        print "----- dataUrl -----"
                        cate = category.split(" ")[0]
                        main_cate = category.split(" ")[1]
                        dataUrl = itemUrl + cate
                        req = scrapy.Request(
                            url=dataUrl, headers=self.headers, callback=self.getDataUrl, dont_filter=True)
                        req.meta['main_cate'] = main_cate

                        # print category
                        # print cate
                        # print main_cate
                        # return

                        yield req
                        # print dataUrl
                        # return
            else:
                for category in self.categories:
                    print "----- dataUrl -----"
                    cate = category.split(" ")[0]
                    main_cate = category.split(" ")[1]
                    dataUrl = countryUrl + cate
                    req = scrapy.Request(
                        url=dataUrl, headers=self.headers, callback=self.getDataUrl, dont_filter=True)
                    req.meta['main_cate'] = main_cate

                    # print category
                    # print cate
                    # print main_cate
                    # return

                    yield req
                    # print dataUrl
                    # return

    def getZoneUrl(self, response):
        print "====== get Zone Urls ======"

        zones = response.xpath(
            '//div[@class="linkshelf-tabs-content zones"]//a[@class="link"]')
        # print len(zones)
        for zone in zones:
            # print "-----------------"
            itemUrl = zone.xpath('@href').extract()[0]

            # print itemUrl
            for category in self.categories:
                print "----- dataUrl -----"
                cate = category.split(" ")[0]
                main_cate = category.split(" ")[1]
                dataUrl = itemUrl + cate
                req = scrapy.Request(
                    url=dataUrl, headers=self.headers, callback=self.getDataUrl, dont_filter=True)
                req.meta['main_cate'] = main_cate

                # print category
                # print cate
                # print main_cate
                # return

                yield req
                # print dataUrl
                # return

    def getDataUrl(self, response):
        print("====== get Detail ======")
        main_cate = response.meta['main_cate']

        products = response.xpath(
            '//div[@class="section_OLXad-list "]/ul[@class="list"]/li[@class="item"]')
        # print len(products)

        for product in products:
            productUrl = product.xpath('a/@href').extract()[0]
            # print "--------- product --------"
            req = scrapy.Request(url=productUrl, headers=self.headers,
                                 callback=self.getDataDetail, dont_filter=True)
            req.meta['main_cate'] = main_cate
            req.meta['productUrl'] = productUrl

            yield req
            # print productUrl
            # return

        nextPage = ''.join(response.xpath(
            '//li[@class="item next"]/a/@href').extract()).strip()
        if nextPage:

            req = scrapy.Request(
                url=nextPage, headers=self.headers, callback=self.getDataUrl, dont_filter=True)
            req.meta['main_cate'] = main_cate
            req.meta['productUrl'] = productUrl

            yield req

    def getDataDetail(self, response):
        main_cate = response.meta['main_cate']
        productUrl = response.meta['productUrl']

        item = OlxscraperItem()

        item['Main_Category'] = main_cate
        item['ADS'] = productUrl

        title = ''.join(response.xpath(
            '//h1[@class="OLXad-title"]/text()').extract()).strip()
        item['Title'] = title
        # print title

        date = ''.join(response.xpath(
            '//div[@class="OLXad-date"]/p/text()').extract()).strip()
        if date:
            date = date.split("em: ")[1].replace(".", "")
            day = date.split(" ")[0]
            month = date.split(" ")[1]
            time = date.split(" ")[2]
            item['Day'] = day
            item['Month'] = month
            item['Time'] = time

        name = ''.join(response.xpath(
            '//li[contains(@class, "item owner")]/p/text()').extract()).strip()
        item['Name'] = name
        # print name

        phone = ""
        phonePath = ''.join(response.xpath(
            '//li[contains(@class, "item phone ")]/span[@id="visible_phone"]/img/@src').extract()).strip()
        if phonePath:
            phone = "http:" + phonePath
        # print phone
        item['Phone'] = phone

        imageUrl = response.xpath('//div[@class="photos"]//a/@href').extract()
        item['Image_urls'] = imageUrl

        mainImageUrl = response.xpath(
            '//div[@class="OLXad-photo-main"]//img/@src').extract()
        item['Main_Image_urls'] = mainImageUrl
        # print imageUrl

        price = ''.join(response.xpath(
            '//span[@class="actual-price"]/text()').extract()).strip()
        item['Price'] = price
        # print price

        description = ''.join(response.xpath(
            '//div[contains(@class, "OLXad-description")]/p/text()').extract()).strip()
        item['Description'] = description
        # print description

        sub_category = ''.join(response.xpath(
            '//div[contains(@class, "OLXad-details")]//ul/li[1]/p/strong/text()').extract()).strip()
        item['Sub_category'] = sub_category
        # print sub_category

        novo_usado = ''.join(response.xpath(
            '//div[contains(@class, "OLXad-details")]//ul/li[2]/p/strong/text()').extract()).strip()
        item['Novo_Usado'] = novo_usado
        # print novo_usado

        city = ''.join(response.xpath(
            '//div[contains(@class, "OLXad-location ")]//ul/li[1]/p/strong/text()').extract()).strip()
        item['City'] = city
        # print city

        suburb = ''.join(response.xpath(
            '//div[contains(@class, "OLXad-location ")]//ul/li[3]/p/strong/text()').extract()).strip()
        item['Suburb'] = suburb
        # print suburb

        zipcode = ''.join(response.xpath(
            '//div[contains(@class, "OLXad-location ")]//ul/li[2]/p/strong/text()').extract()).strip()
        item['zipcode'] = zipcode
        # print zipcode

        adcode = ''.join(response.xpath(
            '//div[@class="OLXad-id"]/p/strong/text()').extract()).strip()
        item['Adcode'] = adcode
        # print adcode

        yield item

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        spider.crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self):
        self.log("Spider idle signal caught.")
        raise DontCloseSpider
