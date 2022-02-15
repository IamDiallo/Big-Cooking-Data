from turtle import color
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from Stats import Stats
from JsonReader import JsonReader

class Clustering:

    def __init__(self, jr):
        self.jr = jr

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
        print("++++++++++++++++++++++++++++++++++++++++++++")
        print("creation du vecteur des recettes")
        # print(np.array(dataset))
        print(raw_data)
        print(len(raw_data))
        print("++++++++++++++++++++++++++++++++++++++++++++")
        
        return recipe_labels, ingredient_labels, np.array(dataset)

    def k_means(self, n_clusters, n_data, dataset=None):
        if dataset is None:
            _, _, dataset = self.get_dataset(n_data)

        # Learning
        pca = PCA(2)
        #Transform the data
        dataset = pca.fit_transform(dataset)
        kmeans = KMeans(n_clusters=n_clusters).fit(dataset)

        # Printing
        for label in range(n_clusters):
            label_index = [i for i, x in enumerate(kmeans.labels_) if x == label]
            recipes = [self.jr.recipes[index] for index in label_index]
            ingredients_ranked = Stats(self.jr).get_ingr_rank(recipes)

            print("\n\nCluster", label, ":")
            ranking_string = ""
            # for index in range(10):
            for index in range(len(ingredients_ranked)):
                ingredient = ingredients_ranked[index]
                if ingredient[0] != 'unique':
                    if ingredient[1][1] != np.nan and ingredient[1][0] != np.nan:
                        ranking_string += ingredient[1][0] + " (" + str(ingredient[1][1]) + "), "
            print(ranking_string + '\n')

            for index_recipe in label_index[:4]:
                self.jr.id = index_recipe
                self.jr.read_recipe()
        
        
        #filter rows of original data
        #predict the labels of clusters.
        kmeans = KMeans(n_clusters=n_clusters)
        label = kmeans.fit_predict(dataset)
        centroids = kmeans.cluster_centers_
        u_labels = np.unique(label)
        for i in u_labels:
            plt.scatter(dataset[label == i , 0] , dataset[label == i , 1] , label = i)
        plt.scatter(centroids[:,0] , centroids[:,1] , s = 80, color="black")
        plt.legend()
        plt.show()
        return kmeans

    def agglomerative(self):
        n_clusters = 3
        n_data = 20
        dataset = self.get_dataset(n_data).reshape(-1, 1)

        # Learning
        model = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward').fit(dataset)
        print("Label : ", model.labels_)
        print("Children :", model.children_)

    def pca(self, n_data):
        def biplot2(pca_components, pca_data, ingredient_labels, recipe_labels, variance_percentage):
            plt.figure(1)

            for sub, place in enumerate([221, 222, 223, 224]):
                plt.subplot(place)
                xvector = pca_components[sub*2]
                yvector = pca_components[sub*2 + 1]
                xs = pca_data[:, sub*2]
                ys = pca_data[:, sub*2 + 1]

                n = len(xvector)
                scalex = 1.0 / (xs.max() - xs.min())
                scaley = 1.0 / (ys.max() - ys.min())

                colors = plt.cm.rainbow(np.linspace(0, 1, 10))

                plt.scatter(xs * scalex, ys * scaley, s=2, c=recipe_labels, label=recipe_labels)
                for i in range(n):
                    if xvector[i]**2 + yvector[i]**2 > 0.15**2:
                        plt.arrow(0, 0, xvector[i], yvector[i], color='r', alpha=0.5)
                        plt.text(xvector[i] * 1.15, yvector[i] * 1.15, ingredient_labels[i], color='r', ha='center', va='center')

                #plt.xlim(-1, 1)
                #plt.ylim(-1, 1)
                plt.xlabel("PC{}".format(1) + "/PC{}".format(sub + 2))
                plt.ylabel("Expl. variance : {0:.3f}".format(variance_percentage[sub]))
                plt.legend()
                plt.grid()
            plt.show()

        # Dataset and labels
        recipe_labels, ingredient_labels, dataset = self.get_dataset(n_data)

        # Learning
        pca = PCA(n_components=dataset.shape[1]).fit(dataset)

        # Percentage of explained variance
        variance_percentage = (pca.explained_variance_ / np.sum(pca.explained_variance_)) * 100
        #print(np.cumsum(pca.explained_variance_) / np.sum(pca.explained_variance_))

        # Kmeans
        kmeans = self.k_means(10, n_data, dataset)
        recipe_labels = kmeans.labels_

        # Drawing
        biplot2(pca.components_, pca.transform(dataset), ingredient_labels, recipe_labels, variance_percentage)

    def generate_labels(self):
        labels = self.k_means(30, 69387).labels_
        self.jr.add_cluster_labels(labels)