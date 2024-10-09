using UnityEditor;
using UnityEngine;
using System.IO;

[InitializeOnLoad]
public static class PlayModeWatcher
{
    private static string logFilePath = "Assets/WPF/play_mode_log.txt"; // Chemin du fichier de log

    static PlayModeWatcher()
    {
        EditorApplication.playModeStateChanged += OnPlayModeStateChanged;
    }

    private static void OnPlayModeStateChanged(PlayModeStateChange state)
    {
        // Écrire dans le fichier log si Unity entre en mode Play
        if (state == PlayModeStateChange.EnteredPlayMode)
        {
            WriteLog("EnteredPlayMode");
        }
        // Écrire dans le fichier log si Unity sort du mode Play
        else if (state == PlayModeStateChange.EnteredEditMode) // Mode Édition
        {
            WriteLog("ExitedPlayMode");
        }
    }

    private static void WriteLog(string message)
    {
        // Écraser le contenu du fichier chaque fois que cette méthode est appelée
        using (StreamWriter writer = new StreamWriter(logFilePath, false)) // false pour écraser le fichier
        {
            writer.WriteLine($"{System.DateTime.Now}: {message}");
        }
    }
}
