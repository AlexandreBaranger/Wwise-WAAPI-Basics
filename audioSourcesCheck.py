import os
import tkinter as tk
from tkinter import filedialog
import json
import subprocess
import ctypes

def show_popup(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Information", 0x40 | 0x1)

def select_directory():
    root = tk.Tk()
    root.withdraw() 
    folder_path = filedialog.askdirectory(title="Sélectionnez un dossier")
    return folder_path
def index_audio_files(folder_path):
    audio_files = []
    audio_extensions = ['.mp3', '.wav', '.ogg']
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                file_path = os.path.normpath(os.path.join(root, file))
                file_name = os.path.splitext(file)[0]
                audio_files.append({'name': file_name, 'path': file_path})
    return audio_files
def write_audio_index_to_json(audio_index, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(audio_index, json_file, ensure_ascii=False, indent=4)
        print(f"Index des fichiers audio écrit avec succès dans {file_path}")
    except Exception as ex:
        print(f"Erreur lors de l'écriture du fichier JSON : {ex}")
if __name__ == "__main__":
    show_popup("Select Work Audio Folder")
    selected_folder = select_directory()
    if selected_folder:
        audio_index = index_audio_files(selected_folder)
        json_file_path = './Data/audioSourceCheck.json'
        write_audio_index_to_json(audio_index, json_file_path)
    else:
        print("Aucun dossier sélectionné.")
subprocess.run(["python", "addAudioToSound.py"])