import os
import numpy as np
import librosa
from scipy.spatial.distance import cdist

# Répertoire contenant les fichiers MP3 de la base de données
database_dir = "mp3/"

# Fonction pour extraire les empreintes acoustiques d'un fichier audio
def extract_features(audio_path):
    y, sr = librosa.load(audio_path, duration=30)  # Chargement du fichier audio
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)  # Calcul du chromagramme
    mfcc = librosa.feature.mfcc(y=y, sr=sr)  # Calcul des coefficients MFCC
    features = np.concatenate((chroma_stft.mean(axis=1), mfcc.mean(axis=1)))  # Concaténation des caractéristiques
    return features

# Chargement de la base de données
database = {}
for filename in os.listdir(database_dir):
    if filename.endswith(".mp3"):
        audio_path = os.path.join(database_dir, filename)
        features = extract_features(audio_path)
        database[filename] = features

# Fonction pour reconnaître une chanson à partir de l'audio du microphone
def recognize_song():
    # Enregistrement de l'audio du microphone
    print("Enregistrement en cours...")
    # Code pour enregistrer l'audio du microphone (utiliser la bibliothèque de votre choix)

    # Extraction des empreintes acoustiques de l'audio enregistré
    recorded_features = extract_features("enregistrement.mp3")

    # Comparaison avec la base de données
    min_distance = float("inf")
    recognized_song = None
    for song, features in database.items():
        distance = cdist([recorded_features], [features], metric="euclidean")[0][0]
        if distance < min_distance:
            min_distance = distance
            recognized_song = song

    if recognized_song:
        print("Chanson reconnue :", recognized_song)
    else:
        print("Aucune chanson reconnue.")

# Appel de la fonction pour reconnaître une chanson
recognize_song()
