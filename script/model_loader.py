# ------------------------
# Cargando modelo de disco
# ------------------------
import tensorflow as tf
from keras.models import load_model

def cargarModelo():

    FILENAME_MODEL_TO_LOAD = "Modelo_RedNeuronal3-60-40.h5"
    MODEL_PATH = "../../model"

    # Cargar la RNA desde disco
    loaded_model = load_model(MODEL_PATH + "/" + FILENAME_MODEL_TO_LOAD)
    print("Modelo cargado de disco << ", loaded_model)

    graph = tf.get_default_graph()
    return loaded_model, graph