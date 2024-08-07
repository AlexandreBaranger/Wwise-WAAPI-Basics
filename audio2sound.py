from waapi import WaapiClient, CannotConnectToWaapiException
import json
import subprocess
import ctypes

def show_popup(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Information", 0x40 | 0x1)

def get_waapi_client():
    try:
        return WaapiClient()
    except CannotConnectToWaapiException as e:
        print(f"Impossible de se connecter à WAAPI : {e}")
        return None
def disconnect_from_waapi(client):
    if client:
        client.disconnect()
        print("Déconnexion de WAAPI")
def get_by_type(client, container_type):
    actor_mixer_query = f"from type {container_type}"
    args = {'waql': actor_mixer_query}
    options = {'return': ['name', 'id', 'path']}
    print(f"Requête WAQL: {actor_mixer_query}")
    try:
        result = client.call("ak.wwise.core.object.get", args, options=options)
        return result.get("return", [])
    except Exception as ex:
        print(f"Erreur lors de l'appel WAAPI : {ex}")
        return []
def write_to_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Résultat écrit avec succès dans {file_path}")
    except Exception as ex:
        print(f"Erreur lors de l'écriture du fichier JSON : {ex}")
if __name__ == "__main__":
    waapi_client = get_waapi_client()    
    if waapi_client:
        sound_objects = get_by_type(waapi_client, 'sound')
        for sound_object in sound_objects:
            sound_object['full_path'] = sound_object['path'] + '/' + sound_object['name']        
        print("Objets de type 'sound' trouvés :", sound_objects)        
        json_file_path = 'Data/soundCheck.json'
        write_to_json(sound_objects, json_file_path)        
        disconnect_from_waapi(waapi_client)
    else:
        print("La connexion à WAAPI a échoué.")
subprocess.run(["python", "audioSourcesCheck.py"])