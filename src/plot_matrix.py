import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn

def plot_confusion_matrix_from_file(file_path):
    # Lese die Confusion-Matrix aus der Textdatei ein
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extrahiere Klassennamen und Confusion-Matrix-Daten aus den Zeilen
    classes = lines[0].strip().split()
    data = [[int(x) for x in line.strip().split()] for line in lines[1:]]

    # Überprüfe die Anzahl der Klassennamen und der Zeilen in der Konfusionsmatrix
    if len(classes) != len(data):
        print("Anzahl der Klassen und Anzahl der Zeilen in der Konfusionsmatrix stimmen nicht überein.")
        return

    # Erstelle einen Heatmap-Plot der Confusion-Matrix
    plt.figure(figsize=(10, 7))
    sn.heatmap(data, annot=True, cmap='Blues', fmt='d', xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.show()

# Beispielaufruf
# Annahme: Die Klassennamen und die Confusion-Matrix sind in der Datei "confusion_matrix.txt" gespeichert
plot_confusion_matrix_from_file("output_files/model/confusion_matrix.txt")
