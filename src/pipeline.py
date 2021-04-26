import pandas as pd
import opensmile
import librosa
from sox import file_info
from math import *
import csv
import os
import time

## 2) Opensmile Feature Extraction (from Feature_Extraction)
## all paths 
## the control and dementia participants all participated in 4 tasks: cookie, sentence, recall, fluency
DATA_PATH = '/content/drive/Shareddrives/Neurologue.ai/ML/'
STORE_PATH = '/content/drive/Shareddrives/Neurologue.ai/ML/Feature_Files/'
DATA_FOLDER = DATA_PATH + 'Pipeline_Input/'

#function to extract audio features from audio file
def OpenSmileAnalysis(file,filename, id):
    store = []
    signal,sr = librosa.load(file, sr=None)
    duration = librosa.get_duration(filename = file, sr=sr) #obtains duration of audio file in seconds
    periods = floor(duration/period) #find number of segments within audio file (in periods)
    if file_info.channels(file) == 1:
        pass
    #if audio is stereo, convert to mono
    elif file_info.channels(file) == 2:
        signal = librosa.to_mono(signal)
    for i in range(periods):
        store.append(SegmentAnalysis(file,signal,sr,i,filename, id))
    return store

#function to extract audio features from slice within audio file
def SegmentAnalysis(file,signal,sr,i,filename,id):
    y = GMAPsmile.process_signal(signal,sampling_rate=sr,start=pd.Timedelta(i*1000000000*period),end=pd.Timedelta((i+1)*1000000000*period))
    y = y.reset_index()
    y.insert(0,"File Name",filename)
    y.insert(0,"Person ID", str(id).zfill(4))
    return y

store = []
GMAPsmile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.GeMAPSv01b,
    feature_level=opensmile.FeatureLevel.Functionals,
    num_channels = 1,
)

period = 2 #time of each audio slice in seconds

#performance timer
starttime = time.perf_counter()

#begin Audio Extraction
print("Beginning audio extraction....")
store = [] #to contain extracted audio data
#scans wav files in one of two folders 'Dementia' or 'Control' (depending on patient) 
#within another 'Audio' folder in your current directoy
data_files = (entry for entry in os.scandir(DATA_FOLDER) if entry.is_file() and "wav" in entry.name)

dict = {'File':[]} #dictionary to contain file name for export
id = 1 #ID assuming that each subject only has one audio file in input
for item in data_files:
    filename = item.name
    file = DATA_FOLDER + item.name
    #save file name into dict
    dict['File'].append(file)
    for item in OpenSmileAnalysis(file,filename, id):
        store.append(item)
    id += 1
        
df = pd.DataFrame(data=dict)
#export dictionary as excel of analyzed files
df.to_csv(STORE_PATH+'patientlist.csv')

#print performance time
print(f"Finished feature extraction in {time.perf_counter()-starttime:0.2f} seconds")

data = store[0]
for item in store[1:]:
    data = data.append(item)
data.head()


## 2.5) Load trained RBF Model + data preparation files (pickle)
## refer to this maybe: https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/
## Will need to apply this in the model code - Classical_Modelling_2ms.ipynb under ML

# Pickle
from sklearn.svm import SVC
import pickle
import numpy as np

## make sure it's same python and library versions
modelfilename = DATA_PATH + 'Modeling/' + 'modelfile' #file for model parameters
scaler = DATA_PATH + 'Modeling/' + 'prepParameters' #file for preprocess parameters
featuredropfilename = DATA_PATH + 'Modeling/' + 'featuresToDrop' #file for features to drop based on preprocessing

# load the model from disk (Classical_Modeling_2ms.ipynb)
loaded_model = pickle.load(open(modelfilename, 'rb'))
loaded_preprocessing = pickle.load(open(scaler, 'rb'))
loaded_todrop = pickle.load(open(featuredropfilename, 'rb'))

## 3) Put Extracted Data into Prediction Model (rbf)
###Function for Preprocessing Data
def preprocess(data, scaler, to_drop):
  data= data.drop(columns=to_drop)
  #scale based on data preparation parameters
  data = pd.DataFrame(scaler.transform(data), columns=data.columns)
  return data

DROP_COLS = ['Person ID','start','end', 'File Name']
data = data.drop(DROP_COLS, axis = 1)
data = preprocess(data, loaded_preprocessing, loaded_todrop)
#preprocessed data, ready for model prediction

result = loaded_model.predict(data)
print(result)
