# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.images import ImagesPipeline
# from scrapy.exceptions import OlxscraperItem
from scrapy.http import Request

from PIL import Image
import pytesseract
import requests
import json


city_data = ['Alto Feliz', 
'Alvorada', 
'Amaral Ferrador', 
'Anta Gorda', 'Arambar\xc3\xa9', 
'Ararica', 
'Arroio Do Meio', 
'Arroio Do Sal', 
'Arroio Do Tigre', 
'Arroio Dos Ratos', 
'Arvorezinha', 
'Balne\xc3\xa1rio Pinhal', 
'Bar\xc3\xa3o', 
'Bar\xc3\xa3o Do Triunfo', 
'Barra Do Ribeiro', 
'Bom Principio', 
'Bom Retiro Do Sul', 
'Boqueir\xc3\xa3o Do Le\xc3\xa3o', 
'Brochier', 
'Buti\xc3\xa1', 
'Cachoeira Do Sul', 
'Cachoeirinha', 
'Camaqu\xc3\xa3', 
'Campo Bom', 'Candel\xc3\xa1ria', 'Canoas', 'Cap\xc3\xa3o Da Canoa', 'Capela De Santana', 'Capit\xc3\xa3o', 'Capivari Do Sul', 'Cara\xc3\xa1', 'Cerro Branco', 'Cerro Grande Do Sul', 'Charqueadas', 'Cidreira', 'Colinas', 'Coqueiro Baixo', 'Cristal', 'Cruzeiro Do Sul', 'Dois Irm\xc3\xa3os', 'Dom Feliciano', 'Dom Pedro De Alc\xc3\xa2ntara', 'Eldorado Do Sul', 'Encantado', 'Encruzilhada Do Sul', 'Estancia Velha', 'Esteio', 'Estrela', 'Fazenda Vilanova', 'Feliz', 'General C\xc3\xa2mara', 'Glorinha', 'Gravata\xc3\xad', 'Gua\xc3\xadba', 'Harmonia', 'Ibarama', 'Igrejinha', 'Il\xc3\xb3polis', 'Imb\xc3\xa9', 'Imigrante', 'Itati', 'Ivoti', 'Lago\xc3\xa3o', 'Lajeado', 'Lindolfo Collor', 'Linha Nova', 'Maquine', 'Mariana Pimentel', 'Marques De Souza', 'Mato Leit\xc3\xa3o', 'Minas Do Le\xc3\xa3o', 'Montenegro', 'Morrinhos Do Sul', 'Morro Reuter', 'Mostardas', 'Mucum', 'Nova Br\xc3\xa9scia', 'Nova Hartz', 'Nova Santa Rita', 'Novo Hamburgo', 'Os\xc3\xb3rio', 'Palmares Do Sul', 'Pantano Grande', 'Pareci Novo', 'Parob\xc3\xa9', 'Passo Do Sobrado', 'Paverama', 'Poco Das Antas', 'Port\xc3\xa3o', 'Porto Alegre', 'Pouso Novo', 'Presidente Lucena', 'Progresso', 'Putinga', 'Relvado', 'Rio Pardo', 'Riozinho', 'Roca Sales', 'Rolante', 'Salvador Do Sul', 'Santa Clara Do Sul', 'Santa Cruz Do Sul', 'Santa Maria Do Herval', 'Santo Ant\xc3\xb4nio Da Patrulha', 'S\xc3\xa3o Jeronimo', 'S\xc3\xa3o Jos\xc3\xa9 Do Hort\xc3\xaancio', 'S\xc3\xa3o Leopoldo', 'S\xc3\xa3o Sebasti\xc3\xa3o Do Cai', 'S\xc3\xa3o Vendelino', 'Sapiranga', 'Sapucaia Do Sul', 'Segredo', 'Sentinela Do Sul', 'Serio', 'Sert\xc3\xa3o Santana', 'Sinimbu', 'Sobradinho', 'Taba\xc3\xad', 'Tapes', 'Taquara', 'Taquari', 'Tavares', 'Terra De Areia', 'Teut\xc3\xb4nia', 'Torres', 'Tramanda\xc3\xad', 'Travesseiro', 'Tr\xc3\xaas Cachoeiras', 'Tr\xc3\xaas Coroas', 'Tr\xc3\xaas Forquilhas', 'Triunfo', 'Tunas', 'Tupandi', 'Vale Do Sol', 'Vale Real', 'Vale Verde', 'Ven\xc3\xa2ncio Aires', 'Vera Cruz', 'Vespasiano Correa', 'Viam\xc3\xa3o', 'Xangri-La', 'Acegu\xc3\xa1', 'Arroio Do Padre', 'Arroio Grande', 'Bage', 'Candiota', 'Cangu\xc3\xa7u', 'Cap\xc3\xa3o Do Le\xc3\xa3o', 'Cerrito', 'Chui', 'Dom Pedrito', 'Herval', 'Hulha Negra', 'Jaguar\xc3\xa3o', 'Morro Redondo', 'Pedras Altas', 'Pedro Os\xc3\xb3rio', 'Pelotas', 'Pinheiro Machado', 'Piratini', 'Rio Grande', 'Santa Vitoria Do Palmar', 'Santana Da Boa Vista', 'S\xc3\xa3o Jos\xc3\xa9 Do Norte', 'S\xc3\xa3o Louren\xc3\xa7o Do Sul', 'Turu\xc3\xa7u', '\xc3\x81gua Santa', 'Alto Alegre', 'Andr\xc3\xa9 Da Rocha', 'Ant\xc3\xb4nio Prado', 'Aratiba', '\xc3\x81urea', 'Bar\xc3\xa3o De Cotegipe', 'Barra Funda', 'Barrac\xc3\xa3o', 'Barros Cassal', 'Bento Gon\xc3\xa7alves', 'Boa Vista Do Sul', 'Bom Jesus', 'Cacique Doble', 'Camargo', 'Cambara Do Sul', 'Campestre Da Serra', 'Campinas Do Sul', 'Campos Borges', 'Canela', 'Cap\xc3\xa3o Bonito Do Sul', 'Carazinho', 'Carlos Barbosa', 'Casca', 'Caseiros', 'Caxias Do Sul', 'Chapada', 'Charrua', 'Cir\xc3\xadaco', 'Colorado', 'Constantina', 'Coronel Pilar', 'Cotipor\xc3\xa3', 'Coxilha', 'David Canabarro', 'Dois Lajeados', 'Engenho Velho', 'Entre Rios Do Sul', 'Erebango', 'Erechim', 'Ernestina', 'Erval Grande', 'Esmeralda', 'Espumoso', 'Estac\xc3\xa3o', 'Fagundes Varela', 'Farroupilha', 'Faxinalzinho', 'Flores Da Cunha', 'Fontoura Xavier', 'Garibaldi', 'Gaurama', 'Get\xc3\xbalio Vargas', 'Gramado', 'Guabiju', 'Guapor\xc3\xa9', 'Ibia\xc3\xa7\xc3\xa1', 'Ibiraiaras', 'Ibirapuit\xc3\xa3', 'Ibirub\xc3\xa1', 'Ip\xc3\xaa', 'Ipiranga Do Sul', 'Itatiba Do Sul', 'Jacutinga', 'Jaquirana', 'Lagoa Dos Tr\xc3\xaas Cantos', 'Lagoa Vermelha', 'Machadinho', 'Marau', 'Marcelino Ramos', 'Mariano Moro', 'Mato Castelhano', 'Maximiliano De Almeida', 'Montauri', 'Monte Alegre Dos Campos', 'Monte Belo Do Sul', 'Morma\xc3\xa7o', 'Muliterno', 'N\xc3\xa3o-Me-Toque', 'Nonoai', 'Nova Alvorada', 'Nova Araca', 'Nova Bassano', 'Nova Boa Vista', 'Nova P\xc3\xa1dua', 'Nova Petr\xc3\xb3polis', 'Nova Prata', 'Nova Roma Do Sul', 'Paim Filho', 'Parai', 'Passo Fundo', 'Paulo Bento', 'Picada Cafe', 'Pinhal Da Serra', 'Ponte Preta', 'Prot\xc3\xa1sio Alves', 'Quatro Irm\xc3\xa3os', 'Quinze De Novembro', 'Ronda Alta', 'Rondinha', 'Sananduva', 'Santa Tereza', 'Santo Ant\xc3\xb4nio Do Palma', 'Santo Ant\xc3\xb4nio Do Planalto', 'Santo Expedito Do Sul', 'S\xc3\xa3o Domingos Do Sul', 'S\xc3\xa3o Francisco De Paula', 'S\xc3\xa3o Jo\xc3\xa3o Da Urtiga', 'S\xc3\xa3o Jorge', 'S\xc3\xa3o Jos\xc3\xa9 Do Herval', 'S\xc3\xa3o Jos\xc3\xa9 Do Ouro', 'S\xc3\xa3o Jos\xc3\xa9 Dos Ausentes', 'S\xc3\xa3o Marcos', 'S\xc3\xa3o Valentim', 'S\xc3\xa3o Valentim Do Sul', 'Sarandi', 'Selbach', 'Serafina Corr\xc3\xaaa', 'Sert\xc3\xa3o', 'Severiano De Almeida', 'Soledade', 'Tapejara', 'Tapera', 'Tio Hugo', 'Tr\xc3\xaas Arroios', 'Tr\xc3\xaas Palmeiras', 'Trindade Do Sul', 'Uni\xc3\xa3o Da Serra', 'Vacaria', 'Vanini', 'Veran\xc3\xb3polis', 'Viadutos', 'Victor Graeff', 'Vila Flores', 'Vila Langaro', 'Vila Maria', 'Vista Alegre Do Prata', 'Agudo', 'Ajuricaba', 'Alecrim', 'Alegrete', 'Alegria', 'Alpestre', 'Ametista Do Sul', 'Augusto Pestana', 'Barra Do Quarai', 'Boa Vista Das Miss\xc3\xb5es', 'Boa Vista Do Buric\xc3\xa1', 'Boa Vista Do Cadeado', 'Bom Progresso', 'Bossoroca', 'Braga', 'Ca\xc3\xa7apava Do Sul', 'Cacequi', 'Caibat\xc3\xa9', 'Cai\xc3\xa7ara', 'Campina Das Miss\xc3\xb5es', 'Campo Novo', 'C\xc3\xa2ndido God\xc3\xb3i', 'Cap\xc3\xa3o Do Cipo', 'Catu\xc3\xadpe', 'Cerro Grande', 'Cerro Largo', 'Chiapetta', 'Condor', 'Coronel Barros', 'Coronel Bicaco', 'Crissiumal', 'Cruz Alta', 'Dezesseis De Novembro', 'Dois Irm\xc3\xa3os Das Miss\xc3\xb5es', 'Dona Francisca', 'Doutor Maur\xc3\xadcio Cardoso', 'Entre-Ijuis', 'Erval Seco', 'Eug\xc3\xaanio De Castro', 'Faxinal Do Soturno', 'Formigueiro', 'Fortaleza Dos Valos', 'Frederico Westphalen', 'Giru\xc3\xa1', 'Guarani Das Miss\xc3\xb5es', 'Horizontina', 'Humait\xc3\xa1', 'Iju\xc3\xad', 'Independ\xc3\xaancia', 'Inhacor\xc3\xa1', 'Irai', 'Itaara', 'Itacurubi', 'Itaqui', 'Ivor\xc3\xa1', 'Jaboticaba', 'Jacuizinho', 'Jaguari', 'Jari', 'Joia', 'J\xc3\xbalio De Castilhos', 'Lavras Do Sul', 'Liberato Salzano', 'Ma\xc3\xa7ambara', 'Manoel Viana', 'Mata', 'Miragua\xc3\xad', 'Nova Esperan\xc3\xa7a Do Sul', 'Nova Palma', 'Novo Barreiro', 'Novo Machado', 'Novo Tiradentes', 'Palmeira Das Miss\xc3\xb5es', 'Palmitinho', 'Panambi', 'Para\xc3\xadso Do Sul', 'Peju\xc3\xa7ara', 'Pinhal', 'Pinhal Grande', 'Pinheirinho Do Vale', 'Pirap\xc3\xb3', 'Planalto', 'Porto Lucena', 'Porto Mau\xc3\xa1', 'Porto Xavier', 'Quarai', 'Quevedos', 'Redentora', 'Restinga Seca', 'Rodeio Bonito', 'Roque Gonzales', 'Ros\xc3\xa1rio Do Sul', 'Saldanha Marinho', 'Salto Do Jacu\xc3\xad', 'Salvador Das Miss\xc3\xb5es', 'Santa Barbara Do Sul', 'Santa Margarida Do Sul', 'Santa Maria', 'Santa Rosa', 'Santana Do Livramento', 'Santiago', 'Santo \xc3\x82ngelo', 'Santo Ant\xc3\xb4nio Das Miss\xc3\xb5es', 'Santo Augusto', 'Santo Cristo', 'S\xc3\xa3o Borja', 'S\xc3\xa3o Francisco De Assis', 'S\xc3\xa3o Gabriel', 'S\xc3\xa3o Jo\xc3\xa3o Do Pol\xc3\xaasine', 'S\xc3\xa3o Jos\xc3\xa9 Das Miss\xc3\xb5es', 'S\xc3\xa3o Jos\xc3\xa9 Do Inhacor\xc3\xa1', 'S\xc3\xa3o Luiz Gonzaga', 'S\xc3\xa3o Martinho', 'S\xc3\xa3o Martinho Da Serra', 'S\xc3\xa3o Miguel Das Miss\xc3\xb5es', 'S\xc3\xa3o Nicolau', 'S\xc3\xa3o Paulo Das Miss\xc3\xb5es', 'S\xc3\xa3o Pedro Das Miss\xc3\xb5es', 'S\xc3\xa3o Pedro Do Buti\xc3\xa1', 'S\xc3\xa3o Pedro Do Sul', 'S\xc3\xa3o Sepe', 'S\xc3\xa3o Vicente Do Sul', 'Seberi', 'Sede Nova', 'Senador Salgado Filho', 'Silveira Martins', 'Taquaru\xc3\xa7u Do Sul', 'Tenente Portela', 'Toropi', 'Tr\xc3\xaas De Maio', 'Tr\xc3\xaas Passos', 'Tucunduva', 'Tupanciret\xc3\xa3', 'Tuparendi', 'Uruguaiana', 'Vicente Dutra', 'Vila Nova Do Sul', 'Vista Alegre', 
'Vista Gaucha']


class OlxscraperPipeline(object):
    def process_item(self, item, spider):
        phone = None
        try:
            url = item["Phone"]
            im = requests.get(url, stream=True).raw
            img = Image.open(im)
            basewidth = 200
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            img.convert('RGB').save("prev.jpg", "JPEG")
            phone = pytesseract.image_to_string(Image.open("prev.jpg"), config="-psm 6")
            phone = phone.replace("].","1").replace("}",")")
            if "(5" in phone and item["City"] not in city_data:
                phone = phone.replace("(5", "(6")
            phone = phone.replace("(","").replace(")", "").replace(" ","").strip()
            phone = "55{0}".format(phone)
            item["Phone_Number"] = phone
        except:
            item["Phone_Number"] = phone
            pass

        data = {
            "title":item["Title"] if "Title" in item else None,
            "ads": item["ADS"] if "ADS" in item else None,
            "name": item["Name"] if "Name" in item else None,
            "phone": item["Phone"] if "Phone" in item else None,
            "phone_number": item["Phone_Number"] if "Phone_Number" in item else None,
            "price": item["Price"] if "Price" in item else None,
            "description": item["Description"] if "Description" in item else None,
            "sub_category": item["Sub_category"] if "Sub_category" in item else None,
            "novo_usado": item["Novo_Usado"] if "Novo_Usado" in item else None,
            "city": item["City"] if "City" in item else None,
            "suburb": item["Suburb"] if "Suburb" in item else None,
            "zipcode": item["zipcode"] if "zipcode" in item else None,
            "adcode": item["Adcode"] if "Adcode" in item else None,
            "image_urls": item["Image_urls"] if "Image_urls" in item else None,
            "main_image_urls": item["Main_Image_urls"] if "Main_Image_urls" in item else None,
            "day": item["Day"] if "Day" in item else None,
            "month": item["Month"] if "Month" in item else None,
            "time": item["Time"] if "Time" in item else None,
            "main_category": item["Main_Category"] if "Main_Category" in item else None
        }

        url = "http://ec2-13-58-190-193.us-east-2.compute.amazonaws.com:8000/post_data"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return item

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise OlxscraperItem("Item contains no images")
        item['image_paths'] = image_paths
        return item