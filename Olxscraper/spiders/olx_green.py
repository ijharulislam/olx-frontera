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
]

all_urls = []

for url in urls:
    sp = url.split("?")
    for cat in categs:
        f_url = sp[0] + "/" + cat + "?" + sp[1] + " " + cat
        all_urls.append(f_url)


class OlxfcSpider(scrapy.Spider):
    name = "olx_green"
    allowed_domains = ["olx.com"]
    start_urls = (
        'http://www.olx.com.br/brasil?f=c',
    )

    categories = {
        "/veiculos/carros?f=c veiculos",
        "/veiculos/pecas-e-acessorios?f=c veiculos",
        "/veiculos/motos?f=c veiculos",
        "/veiculos/caminhoes-onibus-e-vans?f=c veiculos",
        "/veiculos/barcos-lanchas-e-avioes?f=c veiculos",
        "/servicos?f=c empregos-e-negocios",
        "/industria-comercio-e-agro?f=c empregos-e-negocios",
        "/ofertas-de-emprego?f=c empregos-e-negocios",
        "/procuro-emprego?f=c empregos-e-negocios",
        "/imoveis/venda?f=c imoveis",
        "/imoveis/aluguel?f=c imoveis",
        "/imoveis/lojas-salas-e-outros?f=c imoveis",
        "/imoveis/terrenos?f=c imoveis",
        "/imoveis/temporada?f=c imoveis",
        "/imoveis/lancamentos?f=c imoveis",
        "/celulares?f=c eletronicos-e-celulares",
        "/computadores-e-acessorios?f=c eletronicos-e-celulares",
        "/audio-tv-video-e-fotografia?f=c eletronicos-e-celulares",
        "/videogames?f=c eletronicos-e-celulares",
        "/esportes-e-ginastica?f=c esportes",
        "/ciclismo?f=c esportes",
        "/moveis?f=c para-a-sua-casa",
        "/eletrodomesticos?f=c para-a-sua-casa",
        "/arte-e-decoracao?f=c para-a-sua-casa",
        "/jardinagem-e-construcao?f=c para-a-sua-casa",
        "/cama-mesa-e-banho?f=c para-a-sua-casa",
        "/roupas-e-calcados?f=c moda-e-beleza",
        "/bijouteria-relogios-e-acessorios?f=c moda-e-beleza",
        "/beleza-e-saude?f=c moda-e-beleza",
        "/bolsas-malas-e-mochilas?f=c moda-e-beleza",
        "/instrumentos-musicais?f=c musica-e-hobbies",
        "/livros-e-revistas?f=c musica-e-hobbies",
        "/hobbies-e-colecoes?f=c musica-e-hobbies",
        "/musica-e-filmes?f=c musica-e-hobbies",
        "/antiguidades?f=c musica-e-hobbies",
        "/bebes-e-criancas?f=c bebes-e-criancas",
        "/animais-e-acessorios/cachorros?f=c cachorros",
        "/animais-e-acessorios/outros-animais?f=c outros-animais",
        "/animais-e-acessorios/artigos-para-peixes?f=c artigos-para-peixes",
        "/animais-e-acessorios/cavalos?f=c cavalos",
        "/animais-e-acessorios/gatos?f=c gatos",
        "/animais-e-acessorios/roedores?f=c roedores"
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
            index = index - 1
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
                    # print "----- dataUrl -----"
                    # print category
                    cate = category.split(" ")[0]
                    main_cate = category.split(" ")[1]
                    dataUrl = countryUrl + cate
                    # print cate
                    # print main_cate
                    req = scrapy.Request(
                        url=dataUrl, headers=self.headers, callback=self.getDataUrl, dont_filter=True)
                    req.meta['main_cate'] = main_cate

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
