from flask import Flask, request, redirect, url_for, render_template
import os
import sys
#import modules
import extract 
import model

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')
        
        #return render_template('index.html', prediction_text=output, request="POST")
        return render_template('index.html', request="POST")
    else:
        return render_template("index.html")

@app.route('/predict',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
       ##pipeline for extracting 
        file = 'audio.wav'
        data = extract.main(file)
        #load pickle model and make inference
        output = model.main(data)
        print(output)
        return render_template('index.html', prediction_text=output)

if __name__ == "__main__":
    app.run(host = 'localhost', debug=True)
"""
def predict():

    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Sales should be $ {}'.format(output)
"""