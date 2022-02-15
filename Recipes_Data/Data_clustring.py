

def get_dataset(self, n_data):
    id_link = {}
    raw_data = []
    recipe_labels = []
    ingredient_labels = []
    for r in self.jr.recipes[:n_data]:
        raw = []
        for i in r.get('ingredients', []):
            id = i.get('id_ingre')
            if not id == 'unique':
                if id not in id_link:
                    id_link[id] = len(id_link)
                    ingredient_labels.append(i.get('nom_ingre'))
                raw.append(id_link[id])

        raw_data.append(raw)
        recipe_labels.append(r['nom'])

    dataset = []
    vector_size = len(id_link)
    for i in range(len(raw_data)):
        vector = np.zeros(vector_size)
        for id in raw_data[i]:
            vector[id] = 1
        dataset.append(vector)
    dataset = np.array(dataset).reshape(1, -1)
    return recipe_labels, ingredient_labels, dataset