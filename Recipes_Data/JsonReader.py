import json
'''
json_file = open('marmiton.json', encoding='UTF-8')
data = json_file.read()
recipes = json.loads(data)
#print(type(recipes))

for recipe in recipes:
    print(recipe['id'])

'''
class JsonReader:
    file = r"/Users/mamadoubelladiallo/Documents/ProjetIn/MarmitonScraping/Recipes_Data/marmiton.json"
    id = -1

    def __init__(self):
        json_file = open(self.file, encoding='UTF-8')
        data = json_file.read()
        self.recipes = json.loads(data)
        json_file.close()

    def get_att(self, attribute, dict):
        if dict == 'none':
            return'none'
        return dict.get(attribute, 'none')

    def read_recipe(self):
        r = self.recipes[self.id]
        print('Id_Recette : '+str(self.id))

        # print(self.get_att('nom', r) + '    (' + self.get_att('img_url', r) + ')')
        print(self.get_att('nom', r))

        # print('Personnes ' + str(self.get_att('numberP', r)) + ' / Temps ' + str(self.get_att('time_prepa', r))
        #       + ' - ' + self.get_att('time_cuisson', r) + ' - ' + self.get_att('time_repo', r)
        #       + ' - ' + self.get_att('time_total', r) + ' / Difficuly ' + self.get_att('difficylty', r)
        #       + ' / Budget ' + self.get_att('budget', r)+ '\n')

        print('Ingredients : ', end='')
        for ingredient in r.get('ingredients', []):
            print(self.get_att('quantity', ingredient) + ' ' + self.get_att('nom_ingre', ingredient) + '    ', end='')

        print('\nEtapes : ', end='')
        print("list of etapes commented")
        # for etape in r.get('etape', []):
        #     print(str(self.get_att('titre', etape)) + ' ' + self.get_att('description', etape))

    def add_cluster_labels(self, labels):
        for i, label in enumerate(labels):
            self.recipes[i]['label_cluster'] = int(label)