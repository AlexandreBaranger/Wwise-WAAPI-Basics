from waapi import WaapiClient
import pprint

def get_input():
    input_str = ''
    while True:
        char = input()
        if char:
            input_str = char
            break
    return input_str

# Se connecter au serveur Wwise Authoring API
try:
    client = WaapiClient()
except Exception as e:
    print(f"Erreur lors de la connexion à WAAPI: {e}")
    exit(1)

while True:
    # Demander le nom à rechercher
    search_name = input("Entrez le nom à rechercher (pour tous les éléments) : ")

    # Construire la requête WAQL pour chercher dans les différentes hiérarchies
    queries = {
        "Actor-Mixer Hierarchy": f'$ "\\Actor-Mixer Hierarchy" select descendants where name = /{search_name}/',
        "Events": f'$ "\\Events" select descendants where name = /{search_name}/',        
        "Game Parameters (RTPCs)": f'$ "\\Game Parameters" select descendants where name = /{search_name}/',
        "ShareSets": f'$ "\\Modulators" select descendants where name = /{search_name}/'
    }

    all_results = []

    # Exécuter les requêtes pour chaque hiérarchie
    for hierarchy, query in queries.items():
        print(f"Requête WAQL envoyée pour {hierarchy} : {query}")
        args = {'waql': query}
        options = {'return': ['id', 'type', 'name', 'path']}
        
        try:
            result = client.call("ak.wwise.core.object.get", args, options=options)
            if result and 'return' in result and result['return']:
                print(f"\nRésultats trouvés dans {hierarchy} :")
                pprint.pprint(result)
                all_results.extend(result['return'])
            else:
                print(f"Aucun résultat trouvé dans {hierarchy}.")
        except Exception as e:
            print(f"Erreur lors de la requête WAQL pour {hierarchy}: {e}")
    
    if not all_results:
        print("Aucun objet trouvé pour le nom donné.")
    else:
        # Demander un nouveau nom pour les objets trouvés
        new_name = input(f"Entrez le nouveau nom pour tous les objets portant le nom '{search_name}': ")

        # Parcourir tous les objets trouvés et les renommer si possible
        for obj in all_results:
            old_name = obj['name']
            obj_id = obj['id']
            obj_type = obj['type']

            # Certains types d'objets ne peuvent pas être renommés
            if obj_type in ['WorkUnit']:
                print(f"L'objet '{old_name}' (ID: {obj_id}, Type: {obj_type}) ne peut pas être renommé.")
                continue

            # Extraire la partie avant et après l'underscore (s'il existe)
            if '_' in old_name:
                prefix, suffix = old_name.split('_', 1)  # On sépare à partir du premier '_'
                new_full_name = f"{new_name}_{suffix}"  # On garde le suffixe et on remplace le prefix
            else:
                new_full_name = new_name  # Si pas d'underscore, remplacer tout le nom

            # Renommer l'objet via WAAPI
            rename_args = {
                'object': obj_id,
                'value': new_full_name
            }
            try:
                client.call("ak.wwise.core.object.setName", rename_args)
                print(f"L'objet '{old_name}' (ID: {obj_id}) a été renommé en '{new_full_name}'.")
            except Exception as e:
                print(f"Erreur lors du renommage de l'objet '{old_name}': {e}")

    # Demander à l'utilisateur s'il souhaite effectuer une nouvelle recherche
    print("\nVoulez-vous effectuer une nouvelle recherche ? (O/N): ", end='', flush=True)
    response = get_input().lower()

    if response != 'o':
        break  # Sortir de la boucle si la réponse n'est pas 'O'

# Déconnexion
try:
    client.disconnect()
except Exception as e:
    print(f"Erreur lors de la déconnexion: {e}")
