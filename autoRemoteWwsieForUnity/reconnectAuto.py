import time
import os
from waapi import WaapiClient
import tkinter as tk
from tkinter import filedialog

path_file = "log_file_path.txt"

def select_log_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Log File in Unity project", filetypes=[("Text files", "*.txt")])
    return file_path

def save_log_file_path(file_path):
    with open(path_file, 'w') as f:
        f.write(file_path)
    print(f"Log file path saved: {file_path}")

def load_log_file_path():
    if os.path.exists(path_file):
        with open(path_file, 'r') as f:
            return f.read().strip()
    return None

def monitor_log_file(log_file_path):
    if not os.path.exists(log_file_path):
        print("The log file does not exist.")
        return
    print("Monitoring the log file started...")

def connect_waapi():
    try:
        client = WaapiClient()
        print("Successfully connected to WAAPI.")
        return client
    except Exception as e:
        print(f"Error connecting to WAAPI: {e}")
        return None

def get_available_consoles(client):
    try:
        consoles = client.call("ak.wwise.core.remote.getAvailableConsoles")
        print("Available consoles:", consoles)
        return consoles
    except Exception as e:
        print(f"Error retrieving available consoles: {e}")
        return None

def start_profiler(client, app_name):
    try:
        response = client.call("ak.wwise.core.remote.connect", {
            "host": "127.0.0.1",
            "appName": app_name,
            "commandPort": 62866
        })
        print("Server response:", response)
        if response and response.get("result") == 1:
            print("Profiler started successfully.")
        else:
            print("Failed to start the profiler:", response)
    except Exception as e:
        print(f"Error starting the profiler: {e}")

def autoProfiler(client, log_file_path):
    previous_size = 0
    previous_mtime = 0
    profiler_running = False

    while True:
        current_size = os.path.getsize(log_file_path)
        current_mtime = os.path.getmtime(log_file_path)

        if current_size != previous_size or current_mtime != previous_mtime:
            with open(log_file_path, 'r') as file:
                lines = file.readlines()
                
                for line in lines:
                    line = line.strip()
                    print(line)

                    if "EnteredPlayMode" in line and not profiler_running:
                        start_profiler(client, app_name)
                        print("Starting profiler due to entering play mode.")
                        profiler_running = True

                    if "ExitedPlayMode" in line and profiler_running:
                        print("Stopping profiler due to exiting play mode.")
                        profiler_running = False

            previous_size = current_size
            previous_mtime = current_mtime

        time.sleep(1)

if __name__ == "__main__":
    log_file_path = load_log_file_path()
    if not log_file_path:
        log_file_path = select_log_file()
        save_log_file_path(log_file_path)
    monitor_log_file(log_file_path)
    client = connect_waapi()
    if client:
        consoles = get_available_consoles(client)
        app_name = consoles['consoles'][0]["appName"] if consoles and 'consoles' in consoles else "Unity"
        print(f"Using appName: {app_name}")
        autoProfiler(client, log_file_path)
