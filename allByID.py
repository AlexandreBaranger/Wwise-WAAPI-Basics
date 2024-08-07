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
    search_id = input("Entrez l'ID : ")
    waql_query = f'$ "\\Audio Devices\\Default Work Unit\\System", "{{{search_id}}}"'
    print(f"Requête WAQL envoyée : {waql_query}")    
    args = {'waql': waql_query}
    options = {'return': ['id', 'type', 'name', 'Volume', 'path']}    
    result = client.call("ak.wwise.core.object.get", args, options=options)    
    print("\nRésultat avec ID saisi par l'utilisateur:")
    pprint.pprint(result)    
    print("\nVoulez-vous effectuer une nouvelle recherche ? (O/N): ", end='', flush=True)
    response = get_input().lower()
    if response != 'o':
        break  
client.disconnect()
