import msvcrt
from waapi import WaapiClient

client = WaapiClient()

def get_input():
    input_str = ''
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8')
            if char == '\r':
                break
            input_str += char
            print(char, end='', flush=True)
    return input_str

while True:
    print("Entrez le nom de l'Event à rechercher: ", end='', flush=True)
    search_name = get_input()
    actor_mixer_query = f'$ "\\Events" select descendants where name = /{search_name}/'
    print(f"\nRequête WAQL envoyée : {actor_mixer_query}")
    args = {'waql': actor_mixer_query}
    options = {'return': ['name', 'id', 'path']}
    result = client.call("ak.wwise.core.object.get", args, options=options)
    if result and result.get("return"):
        print("\nID \\Events :")
        for obj in result["return"]:
            print(f"{obj['name']} ({obj['id']}) ({obj['path']})")
    else:
        print("Aucun objet trouvé.")
        print("\nVoulez-vous effectuer une nouvelle recherche ? (O/N): ", end='', flush=True)
    response = get_input().lower()
    if response != 'o':
        break 
