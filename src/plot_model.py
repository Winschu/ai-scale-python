import matplotlib.pyplot as plt

def plot_model_history_from_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    history = {}
    for line in lines:
        key, value = line.strip().split(": ")
        # Hier gehen wir davon aus, dass die Werte in der Datei als Liste gespeichert wurden.
        # Wenn sie in einem anderen Format gespeichert sind, passen Sie die Extraktion entsprechend an.
        history[key] = eval(value)

    # Erstellen Sie den Plot für Genauigkeit und Verlust
    plt.plot(history['accuracy'], label='accuracy')
    plt.plot(history['val_accuracy'], label='val_accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

    plt.plot(history['loss'], label='loss')
    plt.plot(history['val_loss'], label='val_loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

# Beispielaufruf
plot_model_history_from_file("./output_files/model/model_history.txt")