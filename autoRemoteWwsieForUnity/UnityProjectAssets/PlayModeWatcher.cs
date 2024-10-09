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
        // �crire dans le fichier log si Unity entre en mode Play
        if (state == PlayModeStateChange.EnteredPlayMode)
        {
            WriteLog("EnteredPlayMode");
        }
        // �crire dans le fichier log si Unity sort du mode Play
        else if (state == PlayModeStateChange.EnteredEditMode) // Mode �dition
        {
            WriteLog("ExitedPlayMode");
        }
    }

    private static void WriteLog(string message)
    {
        // �craser le contenu du fichier chaque fois que cette m�thode est appel�e
        using (StreamWriter writer = new StreamWriter(logFilePath, false)) // false pour �craser le fichier
        {
            writer.WriteLine($"{System.DateTime.Now}: {message}");
        }
    }
}
