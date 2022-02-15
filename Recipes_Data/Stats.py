import numpy as np
import matplotlib.pyplot as plt

class Stats:
    ingr_rank_min = 2

    def __init__(self, jr):
        self.jr = jr

    #Helper
    def helper(self):
        print("stats param_rank")
        print("stats ingr_rank")
        print("stats ingr_find")

    # Paramètres
    def param_rank(self):
        self.ingr_rank_min = int(input())

    # Dictionnaire des ingredients
    # {id: [name, nb]}
    def get_ingredients(self, recipes):
        dict = {}

        for r in recipes:
            for i in r.get('ingredients', []):
                id = i.get('id_ingre')

                if id in dict:
                    dict[id][1] += 1
                else:
                    if id == 'unique':
                        dict[id] = ['unique', 1]
                    else:
                        dict[id] = [i.get('nom_ingre'), 1]
        return dict

    # Ingredients classé par occurence total
    def ingr_rank(self):
        dict = self.get_ingredients(self.jr.recipes)
        ingredients = sorted(dict.items(), key=lambda i: i[1][1], reverse=True)

        print(len(ingredients), "ingredients : \n")

        for j in range(len(ingredients)):
            i = ingredients[j]
            if i[1][1] >= self.ingr_rank_min:
                print(i[1][0], " (", i[0], ") : ", i[1][1])

    def get_ingr_rank(self, recipes):
        dict = self.get_ingredients(recipes)
        #print(sorted(dict.items(), key=lambda i: i[1][1], reverse=True))
        return sorted(dict.items(), key=lambda i: i[1][1], reverse=True)

    # Trouve un ingredient
    def ingr_find(self):
        dict = self.get_ingredients(self.jr.recipes)
        string = input()
        matching = [key for key, value in dict.items() if string in value[0]]

        for key in matching:
            print(dict[key][0], " (", key, ") : ", dict[key][1])

    # Génère un histogramme de la répartition des ingredients
    def ingr_hist(self):
        dict = self.get_ingredients(self.jr.recipes)
        x = [value[1] for key, value in dict.items()]

        plt.hist(x, bins=30, density=True, range=(0, 500))

        plt.xlabel('Ingredient Frequency')
        plt.ylabel('Probability Density')
        plt.title('Histogram of Ingredients Occurrences')
        #plt.yscale('log')
        plt.show()
        #plt.savefig('Histo.png', transparent=True)
