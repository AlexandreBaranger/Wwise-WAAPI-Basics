from waapi import WaapiClient
import pprint

def get_input():
    input_str = ''
    while True:
        char = input()
        if char:
            break
    return char

client = WaapiClient()
while True:
    search_name = input("Entrez le nom de l'object de l'Actor-Mixer à rechercher : ")
    actor_mixer_query = f'$ "\\Actor-Mixer Hierarchy" select descendants where name = /{search_name}/'
    print(f"Requête WAQL envoyée : {actor_mixer_query}")
    args = {'waql': actor_mixer_query}
    options = {'return': ['id', 'type', 'name', 'Volume', 'path']}
    result = client.call("ak.wwise.core.object.get", args, options=options)
    print("\nRésultat avec ID saisi par l'utilisateur:")
    pprint.pprint(result)
    print("\nVoulez-vous effectuer une nouvelle recherche ? (O/N): ", end='', flush=True)
    response = get_input().lower()
    if response != 'o':
        break 
client.disconnect()
