# -*- coding: utf-8 -*-
"""
1-  You will analyse and check the existing scrapy spider in order to see if it is optimized and if needs any code change in order to have better performance and if any new plugin must be added
2-  You will create a Docker and install there tesseract OCR script in order to change number image to number. After this change will need you take this number, delete any space or symbol on it and ad +55 that is the brazilian code. Make this OCR process optimized, i mean, that do not take to much processing from the spider and make the number of itens/hour scraped goes down
3-  You will install Frontera and set it up. Then you will make that we have a continuous crawling of the spider following an order list that i will provide in excell. After the 13M of Ads are crawled you by Frontera the spider will have to look for new Ads in each state/city/suburb and feed the database having in mind to not revisit all URLs already visited. There are some specific URLs that must have priorities and be revisited daily that will be pointed out in the excell, the other ones follow the normal FIFO cycle. Then maybe is better to create concurrent jobs instead of just one big one
4-  You will create an instance in AWS and store all data in S3 or DB that will receive from scrapinghub all itens data. There you gonna create a rest api using Flesk where any external service, having a specific key, will be able to request and write in DB any of the fields of the item
"""

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
    "veiculos"
    "empregos-e-negocios",
    "imoveis",
]

urls = [
    "http://rj.olx.com.br/rio-de-janeiro-e-regiao?f=p",
    "http://mg.olx.com.br/belo-horizonte-e-regiao?f=p",
    "http://pr.olx.com.br/regiao-de-curitiba-e-paranagua?f=p",
    "http://ba.olx.com.br/grande-salvador?f=p",
    "http://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul?f=p",
    "http://go.olx.com.br/grande-goiania-e-anapolis?f=p",
    "http://pe.olx.com.br/grande-recife?f=p",
    "http://am.olx.com.br/regiao-de-manaus?f=p",
    "http://ce.olx.com.br/fortaleza-e-regiao?f=p",
    "http://pa.olx.com.br/regiao-de-belem?f=p",
    "http://sc.olx.com.br/florianopolis-e-regiao?f=p",
    "http://df.olx.com.br/distrito-federal-e-regiao/brasilia?f=p",
    "http://es.olx.com.br/norte-do-espirito-santo?f=p",
    "http://pb.olx.com.br/paraiba/joao-pessoa?f=p",
    "http://se.olx.com.br/?f=p",
    "http://ma.olx.com.br/regiao-de-sao-luis?f=p",
    "http://mt.olx.com.br/regiao-de-cuiaba?f=p",
    "http://pi.olx.com.br/regiao-de-teresina-e-parnaiba?f=p",
]

all_urls = []

for url in urls:
    sp = url.split("?")
    for cat in categs:
        f_url = sp[0] + "/" + cat + "?" + sp[1] + " " + cat
        all_urls.append(f_url)


class OlxfpSpider(scrapy.Spider):
    name = "olx_yellow"
    allowed_domains = ["olx.com"]
    start_urls = (
        'http://www.olx.com.br/brasil?f=p',
    )

    categories = {
        "/veiculos/carros?f=p veiculos",
        "/veiculos/pecas-e-acessorios?f=p veiculos",
        "/veiculos/motos?f=p veiculos",
        "/veiculos/caminhoes-onibus-e-vans?f=p veiculos",
        "/veiculos/barcos-lanchas-e-avioes?f=p veiculos",
        "/servicos?f=p empregos-e-negocios",
        "/industria-comercio-e-agro?f=p empregos-e-negocios",
        "/ofertas-de-emprego?f=p empregos-e-negocios",
        "/procuro-emprego?f=p empregos-e-negocios",
        "/imoveis/venda?f=p imoveis",
        "/imoveis/aluguel?f=p imoveis",
        "/imoveis/lojas-salas-e-outros?f=p imoveis",
        "/imoveis/terrenos?f=p imoveis",
        "/imoveis/temporada?f=p imoveis",
        "/imoveis/lancamentos?f=p imoveis",
        "/celulares?f=p eletronicos-e-celulares",
        "/computadores-e-acessorios?f=p eletronicos-e-celulares",
        "/audio-tv-video-e-fotografia?f=p eletronicos-e-celulares",
        "/videogames?f=p eletronicos-e-celulares",
        "/esportes-e-ginastica?f=p esportes",
        "/ciclismo?f=p esportes",
        "/moveis?f=p para-a-sua-casa",
        "/eletrodomesticos?f=p para-a-sua-casa",
        "/arte-e-decoracao?f=p para-a-sua-casa",
        "/jardinagem-e-construcao?f=p para-a-sua-casa",
        "/cama-mesa-e-banho?f=p para-a-sua-casa",
        "/roupas-e-calcados?f=p moda-e-beleza",
        "/bijouteria-relogios-e-acessorios?f=p moda-e-beleza",
        "/beleza-e-saude?f=p moda-e-beleza",
        "/bolsas-malas-e-mochilas?f=p moda-e-beleza",
        "/instrumentos-musicais?f=p musica-e-hobbies",
        "/livros-e-revistas?f=p musica-e-hobbies",
        "/hobbies-e-colecoes?f=p musica-e-hobbies",
        "/musica-e-filmes?f=p musica-e-hobbies",
        "/antiguidades?f=p musica-e-hobbies",
        "/bebes-e-criancas?f=p bebes-e-criancas",
        "/animais-e-acessorios/cachorros?f=p cachorros",
        "/animais-e-acessorios/outros-animais?f=p outros-animais",
        "/animais-e-acessorios/artigos-para-peixes?f=p artigos-para-peixes",
        "/animais-e-acessorios/cavalos?f=p cavalos",
        "/animais-e-acessorios/gatos?f=p gatos",
        "/animais-e-acessorios/roedores?f=p roedores"
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
        for u in all_urls:
            url = u.split(" ")[0]
            main_cate = u.split(" ")[1]
            req = scrapy.Request(url=url, headers=self.headers,
                                 callback=self.getDataUrl, dont_filter=True)
            req.meta['main_cate'] = main_cate
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
            req.meta['productUrl'] = productUrl
            req.meta['main_cate'] = main_cate

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
