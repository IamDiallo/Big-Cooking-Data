from JsonReader import JsonReader
from Stats import Stats
from Prototype import Prototype
from Clustering import Clustering

close = False
json = JsonReader()
stats = Stats(json)
recommender = Prototype(json)
clustering = Clustering(json)



def user_command():
    global close
    command = input()

    # Id recipe
    if command.isdigit():
        json.id = int(command)
        json.read_recipe()

    # Next recipe
    elif not command:
        json.id += 1
        json.read_recipe()

    # Appel au module stats
    elif command.find('stats ') != -1:
        command = command.replace('stats ', '')
        getattr(stats, command)()

    elif command.find('stats') != -1:
        stats.helper()

    # Appel au module prototype
    elif command.find('recommender ') != -1:
        command = command.replace('recommender ', '')
        getattr(recommender, command)()

    elif command.find('recommender') != -1:
        recommender.helper()

    # Appel au module cluster
    elif command.find('cluster') != -1:
        command = command.replace('cluster ', '')
        #getattr(clustering, command)()
        clustering.k_means(3, 20)
        # clustering.agglomerative()

    # Exit
    elif command == 'exit':
        close = True

    else:
        print("Unknow command !\n")


def main():

    print('Fichier ouvert avec ' + str(len(json.recipes)) + ' recettes\n')
    print('Taper un id de recette')
    print('Appuyer sur entré pour les faire défilé\n')
    print('"create_db" pour créer ou recrée la base')
    print('"build_db" pour remplir la base avec les recettes')
    print('"truncate_db" pour supprimer la table recipe')
    print('"stats" pour le module de statistique')
    print('"recommender" pour le module de recommendation')
    print('"exit" pour fermé')

    while not close:
        print()
        user_command()


main()
