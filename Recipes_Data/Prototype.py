class Prototype:
    k_best_recipes = 5
    scores = {}

    def __init__(self, jr):
        self.jr = jr

    # Helper
    def helper(self):
        print("recommender param_k")
        print("recommender add_ingr")
        print("recommender best_recipes")

    # Paramètres
    def param_k(self):
        self.k_best_recipes = int(input())

    # Ajouter des ingrediens à la matrice des scores
    def add_ingr(self):
        string = input()

        for ingr in string.split(", "):
            id, score = ingr.split(" ")
            self.scores[id] = int(score)

    # Trouve les meilleures recettes
    def best_recipes(self):
        recipes_score = [self.score_recipe(recipe) for recipe in self.jr.recipes]
        index_best = sorted(range(len(recipes_score)), key=lambda k: recipes_score[k], reverse=True)

        for index in index_best[:self.k_best_recipes]:
            print("Score : ", recipes_score[index])
            self.jr.id = index
            self.jr.read_recipe()
            print("\n")

    def score_recipe(self, r):
        score = 0
        ingr_cumul = {}

        for ingredient in r.get('ingredients', []):
            id = ingredient['id']
            if id in ingr_cumul:
                ingr_cumul[id] += 1
            else:
                ingr_cumul[id] = 1

        for id, occur in ingr_cumul.items():
            score += self.score_ingredient(id, occur)

        return score

    def score_ingredient(self, id, occur):
        return self.scores.get(id, 0) * (1 + 0.7 * (occur-1))
