from waapi import WaapiClient, CannotConnectToWaapiException

def get_waapi_client():
    try:
        return WaapiClient()
    except CannotConnectToWaapiException as e:
        print(f"Impossible de se connecter à WAAPI : {e}")
        return None

def disconnect_from_waapi(client):
    if client:
        client.disconnect()

def get_by_type(client, container_type):
    actor_mixer_query = f'from type {container_type}'
    args = {'waql': actor_mixer_query}
    options = {'return': ['name', 'id']}
    print(f"Requête WAQL: {actor_mixer_query}")
    try:
        result = client.call("ak.wwise.core.object.get", args, options=options)
        return result.get("return", [])
    except Exception as ex:
        print(f"Erreur lors de l'appel WAAPI : {ex}")
        return []

def nouvelle_recherche():
    return input("Voulez-vous effectuer une nouvelle recherche ? (Oui/Non): ").lower().startswith('o')
if __name__ == "__main__":
    waapi_client = get_waapi_client()
    if waapi_client:
        try:
            while True:
                print("Choisissez le type de container:")
                print("1. BlendContainer")
                print("2. RandomSequenceContainer")
                print("3. SwitchContainer")
                container_choice = input("Entrez le numéro du type de container à rechercher (1, 2, 3): ")
                container_types = ["BlendContainer", "RandomSequenceContainer", "SwitchContainer"]
                if container_choice.isdigit() and 1 <= int(container_choice) <= len(container_types):
                    selected_type = container_types[int(container_choice) - 1]
                    containers = get_by_type(waapi_client, selected_type)
                    if containers:
                        print(f"Containers trouvés de type {selected_type}:")
                        for container in containers:
                            print(f"Nom: {container['name']}, ID: {container['id']}")
                    else:
                        print("Aucun container trouvé.")
                else:
                    print("Choix de container invalide.")
                if not nouvelle_recherche():
                    break
        finally:
            disconnect_from_waapi(waapi_client)
