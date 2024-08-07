from waapi import WaapiClient
import pprint

def get_input():
    input_str = ''
    while True:
        char = input()
        if char:
            break
    return char

# Se connecter au serveur Wwise Authoring API
client = WaapiClient()

while True:
    # Demander le nom à rechercher (début du nom avec '^')
    search_name = input("Entrez le nom de l'Event à rechercher: ")

    # Construire la requête WAQL pour récupérer les objets sous la hiérarchie du Actor-Mixer avec le nom recherché
    actor_mixer_query = f'$ "\\Events" select descendants where name = /{search_name}/'
    print(f"Requête WAQL envoyée : {actor_mixer_query}")

    args = {'waql': actor_mixer_query}
    options = {'return': ['id', 'type', 'name', 'path']}

    # Récupérer les résultats de la requête WAQL
    result = client.call("ak.wwise.core.object.get", args, options=options)

    # Afficher les résultats de la requête avec l'ID saisi par l'utilisateur
    print("\nRésultat avec ID saisi par l'utilisateur:")
    pprint.pprint(result)

    # Demander à l'utilisateur s'il souhaite effectuer une nouvelle recherche
    print("\nVoulez-vous effectuer une nouvelle recherche ? (O/N): ", end='', flush=True)
    response = get_input().lower()

    if response != 'o':
        break  # Sortir de la boucle si la réponse n'est pas 'O'

# Déconnexion
client.disconnect()
