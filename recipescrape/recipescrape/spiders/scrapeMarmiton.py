import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = False
FIELDS = [
   'id','nom', 'img_url', 'time', 'difficylty', 'budget','numberP',
   'ingredients','id_ingre','nom_ingre', 'quantity','image_ingre'
]


def getFloat(x, index=0):
    # extracts only the numerical portion of text
    try:
        return float(re.findall(r'[-+]?[0-9]*\.?[0-9]+', x)[index])
    except:
        return 0.0


def getText(x, index=0, toLower=False):
    # extracts only the alphabetical portion of text
    temp = []
    try:
        for world in x:
            if(world!="\xa0"):
                temp.append(world)
        return temp

    except:
        return 'error'


def delSpaces(x):
    # strips and removes annoying carriage returns
    return x.translate({ord(c): None for c in u'\r\n\t'}).strip()

class Marmiton(CrawlSpider):
    name = 'marmiton'
    allowed_domains = ['marmiton.org']

    start_urls = [ 'https://www.marmiton.org/recettes?page=2']
    
    # first get the next button which will visit every page of a category
    rule_next = Rule(LinkExtractor(
                    restrict_xpaths=('.//nav[@class="af-pagination"]/ul/li/a')
                    ),
                    follow=True,
                    )

     # secondly # Extract links matching 'recipe' and parse them with the spider's method parse_item
    rule_recipe = Rule(LinkExtractor(allow=('https://www.marmiton.org/recettes/'), unique=True),
                       callback='parse_item',
                       follow=True,
                       )
    rules = (rule_recipe, rule_next)
    item_index =-2
    def parse_item(self, response):
        if DEBUG:
            self.state['items_count'] = self.state.get('items_count', 0) + 1
            self.log(
                f"{self.state['items_count']} {response.url}", logging.WARN)
        try:
            img_recette_url = response.css(".SHRD__sc-dy77ha-0.vKBPb::attr(src)").extract_first()
            name = response.css('h1.SHRD__sc-10plygc-0.itJBWW::text').get()
            infosRecette  = response.xpath('.//span[@class="SHRD__sc-10plygc-0 cBiAGP"]/p/text()').getall()
            time = infosRecette[0]
            difficulty = infosRecette[1]
            budget = infosRecette[2]
            number_people = 1
            infos_ingre = response.css('div.MuiGrid-root')
            ingre_table = []
            ingre_dic = {}
            for index, link in enumerate(infos_ingre):
                img_ingre_url = link.xpath('.//div[@class="RCP__sc-vgpd2s-2 fNmocT"]/picture/img/@src').get()
                qty_ingre = link.xpath('.//span[@class="SHRD__sc-10plygc-0 epviYI"]/text()').extract()[0]
                nom_ingre = link.xpath('.//span[@class="RCP__sc-8cqrvd-3 itCXhd"]/text()').get()
                if(nom_ingre == None):
                    nom_ingre = link.xpath('.//span[@class="RCP__sc-8cqrvd-3 cDbUWZ"]/text()').get()
                if(qty_ingre == None):
                    qty_ingre = 'empty'
                ingre_dic={"id_ingre":index,"nom_ingre":nom_ingre,"quantity":qty_ingre,"image_ingre":img_ingre_url}
                ingre_table.append(ingre_dic)
        except:
              print('error: on selecting info')
        self.item_index += 1
        data = {
                'id':self.item_index,
                'nom':name,
                'img_url': img_recette_url,
                'time': time, 
                'difficylty':difficulty, 
                'budget':budget ,
                'numberP':number_people ,
                'ingredients' :ingre_table

           }
        dataDic = {}
        dataDic.update(data)
        yield dataDic
    
