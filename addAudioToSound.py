from waapi import WaapiClient
import json
import subprocess
import ctypes

def show_popup(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Information", 0x40 | 0x1)

# Charger les données des fichiers JSON
with open('./Data/audioSourceCheck.json', 'r') as audio_source_file:
    audio_source_data = json.load(audio_source_file)

with open('./Data/soundCheck.json', 'r') as sound_file:
    sound_data = json.load(sound_file)

# Initialiser la liste pour stocker les correspondances à l'extérieur de la boucle
correspondences = []

# Se connecter au serveur Wwise Authoring API
with WaapiClient() as client:
    try:
        for audio_source_entry in audio_source_data:
            audio_name = audio_source_entry['name']
            audio_path = audio_source_entry['path']

            # Trouver la correspondance du parent sound
            matching_parent = next((sound for sound in sound_data if sound['name'] == audio_name), None)

            if matching_parent:
                parent_full_path = matching_parent['path']

                # Vérifier si le child existe déjà
                existing_child_names = [child['name'] for child in matching_parent.get('sound', [])]
                if audio_name in existing_child_names:
                    print(f"Enfant {audio_name} déjà existant sous {parent_full_path}.")
                else:
                    new_child_entry = {
                        "name": audio_name,
                        "type": "AudioFileSource",
                        "import": {
                            "files": [{"audioFile": audio_path}]
                        }
                    }

                    correspondences.append({
                        'full_path': parent_full_path,
                        'pathchild': audio_path
                    })

                    print(f"Correspondance utilisée pour la requête : {json.dumps(correspondences[-1], indent=2)}")
                    print(f"Enfant {audio_name} ajouté sous {parent_full_path} -> {audio_path}")

                    # Enregistrez les correspondances dans le fichier correspondancesAudioSound.json
                    with open('./Data/correspondancesAudioSound.json', 'w') as correspondences_file:
                        json.dump(correspondences, correspondences_file, indent=2)

                    # Envoyer la requête pour créer le child audio source
                    action_args = {
                        'objects': [
                            {
                                'object': parent_full_path,
                                'children': [
                                    {
                                        'name': audio_name,
                                        'type': 'AudioFileSource',
                                        'import': {
                                            'files': [{"audioFile": audio_path}]
                                        }
                                    }
                                ]
                            }
                        ]
                    }

                    print(f"Commande de la requête : {json.dumps(action_args, indent=2)}")

                    action_result = client.call("ak.wwise.core.object.set", action_args)

                    if action_result and 'return' in action_result and action_result['return']:
                        print(f"Action 'Create' pour l'enfant {audio_name} réussie.")
                    else:
                        print(f"Erreur lors de la création de l'enfant {audio_name}. Vérifiez les données d'entrée.")
            else:
                print(f"Aucun parent correspondant trouvé pour {audio_name}.")

    except Exception as e:
        print(f"Une erreur s'est produite: {e}")

client.disconnect()
show_popup("Audio set on Sound Object Done - Save Wwise project and reaload project")