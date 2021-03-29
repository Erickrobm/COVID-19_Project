# Importar librerias de Flask.
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS

# Importar librerias de Keras para trabajar con imagenes.
from keras.preprocessing import image

# Importar las librerias de Python y cargar función "cargarModelo"
# de script "model_loader".
import numpy as np

import requests
import json
import os
from werkzeug.utils import secure_filename
from model_loader import cargarModelo

# Constante que crea carpeta para almacenar imágenes que se coloquen.
UPLOAD_FOLDER = '../images/uploads'
# Set de extensiones de archivos permitidos.
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Número de puerto por default.
port = int(os.getenv('PORT', 5000))
print ("Port recognized: ", port)

#Initialize the application service
app = Flask(__name__)
CORS(app)
# Variables globales para contener el modelo, mandar a llamar script "model_loader.py".
global loaded_model, graph
loaded_model, graph = cargarModelo()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Validación de extensión de las imágenes (.jpg, .jpeg y .png).
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Definir ruta que devuelve cadena de string en el path raíz del web service.
@app.route('/')
def main_page():
	return '¡Servicio REST activo!'

# Ruta para acceder al BackEnd de Python.
@app.route('/model/covid19/', methods=['GET','POST'])
def default():
    data = {"success": False}
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            print('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADBoolean type_FOLDER'], filename))

            # Almacenando imagen en variable.
            filename = UPLOAD_FOLDER + '/' + filename
            print("\nfilename:",filename)

            image_to_predict = image.load_img(filename, target_size=(64,64))
            test_image = image.img_to_array(image_to_predict)
            test_image = np.expand_dims(test_image, axis = 0)
            test_image = test_image.astype('float32')
            test_image /= 255

            with graph.as_default():
            	result = loaded_model.predict(test_image)[0][0]
            	# print(result)
            	
	# Resultados
    if(result[0][0]>result[0][1] and result[0][0]>result[0][2]): 
        prediction = 0

    elif(result[0][1]>result[0][0] and result[0][1]>result[0][2]): 
        prediction = 1    

    else: prediction = 2
                
    CLASSES = ["NORMAL", "COVID-19", "Viral Pneumonia"]

    ClassPred = CLASSES[prediction]
    ClassProb = result
            	
    print("Diagnóstico del Paciente:", ClassPred)
    print("Probabilidad: {:.2f}".format(ClassProb), "%")

    #Results as Json
    data["predictions"] = []
    r = {"label": ClassPred, "score": float(ClassProb)}
    data["predictions"].append(r)

    #Success
    data["success"] = True
    
    return jsonify(data)

# Run de application
app.run(host='0.0.0.0',port=port, threaded=False)