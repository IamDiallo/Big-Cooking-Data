from scrapy.spiders import SitemapSpider
import re

class MySpider(SitemapSpider):
    name = "scrap_sitemap"
    #Use of the sitemap module
    sitemap_urls = ['http://www.marmiton.org/wsitemap_index.xml']
    sitemap_rules = [
        ('/recettes/', 'parse_recettes'),
    ]

    def parse_recettes(self, response):
        #Image parsing
        image_urls = []

        #Time parsing
        time = {}
        total = ('total', response.css(".title-2.recipe-infos__total-time__value::text").extract_first())
        preparation = ('preparation', response.css(".recipe-infos__timmings__preparation .recipe-infos__timmings__value::text").extract_first())
        cooking = ('cooking', response.css(".recipe-infos__timmings__cooking .recipe-infos__timmings__value::text").extract_first())
        safe_insert(total, time)
        safe_insert(preparation, time)
        safe_insert(cooking, time)
        
        #Ingredients parsing
        ingredients = []
        ingredients_selector = response.css(".recipe-results fix-inline-block")
        for ingredient in ingredients_selector:
            dict_ingredient = {}
            full_name = ingredient.css(".recipe-card__title::text").extract_first()
            prefix = ('prefix', re.split("  |' ", full_name)[0])
            name = ('name', re.split("  |' ", full_name)[1])
            complement = ('complement', ingredient.css(".recipe-ingredient__complement::text").extract_first())
            quantity = ('quantity', ingredient.css(".recipe-ingredient-qt::text").extract_first())
            image_url = ingredient.css(".lazyloaded::attr(src)").extract_first()
            id = ('id', image_url.split('/')[-1].split('_')[0].replace('ingredient', 'unique'))
            image_urls.append(image_url)
            safe_insert(id, dict_ingredient)
            safe_insert(prefix, dict_ingredient)
            safe_insert(name, dict_ingredient)
            safe_insert(complement, dict_ingredient)
            safe_insert(quantity, dict_ingredient)

            ingredients.append(dict_ingredient)
        
        #Utensils parsing
        utensils = []
        utensils_selector = response.css(".recipe-utensil__name::text").extract()
        for utensil in utensils_selector:
            ustensil = utensil.strip("\r\n\t")
            if ustensil != "":
                utensils.append(ustensil)
        
        #Etapes parsing
        etapes = []
        etapes_selector = response.css(".recipe-preparation__list__item")
        for i, etape in enumerate(etapes_selector):
            description = ""
            for string in etape.css("::text").extract():
                description += string.strip("\r\n\t")
            
            dict = {
                'Etape' : i + 1,
                'Description' : description.replace("Etape " + str(i+1), '', 1)
            }
            etapes.append(dict)
        
        #Main parsing
        scraped_recipe = {'url': response.url, 'image_urls': image_urls}
        
        title = ('title', response.css("h1.main-title::text").extract_first())
        number_of_person = ('number_of_person', response.css(".title-2.recipe-infos__quantity__value::text").extract_first())
        rating = ('rating', response.css(".recipe-reviews-list__review__head__infos__rating__value::text").extract_first())
        level = ('level', response.css(".recipe-infos__level").xpath("div/@class").re_first(".$"))
        budget = ('budget', response.css(".recipe-infos__budget").xpath("div/@class").re_first(".$"))
        categories = ('categories', response.css(".mrtn-tag--grey::text").extract())

        safe_insert(title, scraped_recipe)
        safe_insert(number_of_person, scraped_recipe)
        safe_insert(rating, scraped_recipe)
        safe_insert(level, scraped_recipe)
        safe_insert(budget, scraped_recipe)
        safe_insert(categories, scraped_recipe)
        safe_insert(('time', time), scraped_recipe)
        safe_insert(('ingredients', ingredients), scraped_recipe)
        safe_insert(('utensils', utensils), scraped_recipe)
        safe_insert(('etapes', etapes), scraped_recipe)
        
        yield scraped_recipe
    
#Insert in the dict valid data
def safe_insert(data, dictio):
    (name, value) = data

    if isinstance(value, str) and value is not None and not value.isspace() and value != "":
        dictio[name] = value.strip("\r\n\t")

    elif isinstance(value, list) and value:
        dictio[name] = value

    elif isinstance(value, dict) and value:
        dictio[name] = value