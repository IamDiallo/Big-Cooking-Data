import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = False
FIELDS = [
   'id','url','nom', 'img_url','time_total', 'time_prepa','time_repo','time_cuisson', 'difficylty', 'budget','numberP','etape', 'etap_id','titre', 'description',
   'id_ingre0','nom_ingre0', 'quantity0','image_ingre0',
   'id_ingre1','nom_ingre1', 'quantity1','image_ingre1',
   'id_ingre2','nom_ingre2', 'quantity2','image_ingre2',
   'id_ingre3','nom_ingre3', 'quantity3','image_ingre3',
   'id_ingre4','nom_ingre4', 'quantity4','image_ingre4',
   'id_ingre5','nom_ingre5', 'quantity5','image_ingre5',
   'id_ingre6','nom_ingre6', 'quantity6','image_ingre6',
   'id_ingre7','nom_ingre7', 'quantity7','image_ingre7',
   'id_ingre8','nom_ingre8', 'quantity8','image_ingre8',
   'id_ingre9','nom_ingre9', 'quantity9','image_ingre9',
   'id_ingre10','nom_ingre10', 'quantity10','image_ingre10',
   'id_ingre11','nom_ingre11', 'quantity11','image_ingre11'
   'id_ingre12','nom_ingre12', 'quantity12','image_ingre12'
   'id_ingre13','nom_ingre13', 'quantity13','image_ingre13'
   'id_ingre14','nom_ingre14', 'quantity14','image_ingre14'
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
    listQty =[]
    for i in x:
       if(i!="\xa0"):
        listQty.append(i)
    return listQty

class Marmiton(CrawlSpider):
    name = 'marmiton'
    allowed_domains = ['marmiton.org']

    start_urls = [ 
        #'https://www.marmiton.org/recettes?type=platprincipal',
        'https://www.marmiton.org/recettes?page=2'
        ]
    
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
    item_index =-1
    def parse_item(self, response):
        ingre_table = []
        etape_tab = []
        data = {}
        if DEBUG:
            self.state['items_count'] = self.state.get('items_count', 0) + 1
            self.log(
                f"{self.state['items_count']} {response.url}", logging.WARN)
        try:
            img_recette_url = response.css(".SHRD__sc-dy77ha-0.vKBPb::attr(src)").extract_first()
            name = response.css('h1.SHRD__sc-10plygc-0.itJBWW::text').get()
            infosRecette  = response.xpath('.//span[@class="SHRD__sc-10plygc-0 cBiAGP"]/p/text()').getall()
            time = response.xpath('.//span[@class="SHRD__sc-10plygc-0 bzAHrL"]/text()').getall()
            time_prepa = time[1]
            time_repo = time[2]
            time_cuisson = time[3]
            time = infosRecette[0]
            difficulty = infosRecette[1]
            budget = infosRecette[2]
            number_people = 1
            etapes = response.css('div.SHRD__sc-juz8gd-3')
            etape_infos = etapes.css("ul li")
            
            for i, etape in enumerate(etape_infos):
                titre = etape.xpath('.//div[@class="RCP__sc-1wtzf9a-0 hXKiLp"]/h3/text()').get()
                description = etape.xpath('.//p[@class="RCP__sc-1wtzf9a-3 jFIVDw"]/text()').get()
                etape_dic = {'etap_id':i,'titre':titre, 'description':description}
                etape_tab.append(etape_dic)

            infos_ingre = response.css('div.MuiGrid-root')
            self.item_index += 1
            data = {
                'id':self.item_index,
                'url': response.url,
                'nom':name,
                'img_url': img_recette_url,
                'time_total': time,
                'time_prepa': time_prepa, 
                'time_repo': time_repo, 
                'time_cuisson': time_cuisson, 
                'difficylty':difficulty, 
                'budget':budget ,
                'numberP':number_people ,
                'etape':etape_tab
           }
            for index, link in enumerate(infos_ingre):
                img_ingre_url = link.xpath('.//div[@class="RCP__sc-vgpd2s-2 fNmocT"]/picture/img/@src').get()
                qty_ingre = link.xpath('.//span[@class="SHRD__sc-10plygc-0 epviYI"]/text()').extract_first()
                nom_ingre = link.xpath('.//span[@class="RCP__sc-8cqrvd-3 itCXhd"]/text()').get()
                qty = link.css('span.epviYI::text').get()
                if(nom_ingre == None):
                    nom_ingre = link.xpath('.//span[@class="RCP__sc-8cqrvd-3 cDbUWZ"]/text()').get()
                # ingre_dic={"id_ingre":index,"nom_ingre":nom_ingre,"quantity":qty_ingre,"image_ingre":img_ingre_url}
                # ingre_table.append(ingre_dic)
                nom = 'nom_ingre' + str(index)
                quantity = 'quantity' + str(index)
                if index !=0:
                    data.update({
                        nom:nom_ingre, 
                        quantity:qty_ingre,
                    })
            yield data
        except:
              print('error: on selecting info')
        # dataDic = {}
        # dataDic.update(data)
       
        # yield dataDic
    
