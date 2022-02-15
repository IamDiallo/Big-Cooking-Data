import json
'''
json_file = open('marmiton.json', encoding='UTF-8')
data = json_file.read()
recipes = json.loads(data)
#print(type(recipes))

for recipe in recipes:
    print(recipe['id'])

'''
json_file = open('marmiton.json', encoding='UTF-8')
data = json_file.read()
recipes = json.loads(data)

def get_att(attribute, dict):
    if dict == 'none':
        return'none'
    return dict.get(attribute, 'none')

def read_recipe(id):
    r = recipes[id]
    print('Id : '+str(id))

    print(get_att('nom', r) + '    (' + get_att('img_url', r) + ')')

    print('Personnes ' + str(get_att('numberP', r)) + ' / Temps ' + str(get_att('time_prepa', r))
          + ' - ' + get_att('time_cuisson', r) + ' - ' + get_att('time_repo', r)
          + ' - ' + get_att('time_total', r) + ' / Difficuly ' + get_att('difficylty', r)
          + ' / Budget ' + get_att('budget', r)+ '\n')

    print('Ingredients : ', end='')
    for ingredient in r.get('ingredients', []):
        print(get_att('quantity', ingredient) + ' ' + get_att('nom_ingre', ingredient) + '    ', end='')

    print('\nEtapes : ', end='')
    for etape in r.get('etape', []):
        print(str(get_att('titre', etape)) + ' ' + get_att('description', etape))

read_recipe(2000)