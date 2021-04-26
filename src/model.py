from sklearn.svm import SVC
import pickle
import numpy as np
import os
import sys
import pandas as pd

## make sure it's same python and library versions


# load the model from disk (Classical_Modeling_2ms.ipynb)


## 3) Put Extracted Data into Prediction Model (rbf)
###Function for Preprocessing Data
def preprocess(data, scaler, to_drop):
  data= data.drop(columns=to_drop)
  #scale based on data preparation parameters
  data = pd.DataFrame(scaler.transform(data), columns=data.columns)
  return data

def finalCall(data):
    resultarray = np.array(data)
    cnttrue = 0
    cntfalse = 0
    cntfalse = (resultarray == 0).sum()
    cnttrue = (resultarray == 1).sum()
    value1 = 100*cnttrue/(cntfalse + cnttrue)
    value2 = abs(100-value1)
    if cnttrue > cntfalse:
        output = "Likely dementia, percentage: " + str(value1) + "%"
        return output
    elif cnttrue < cntfalse:
        output = "Likely healthy, percentage: " + str(value2) + "%"
        return output
    else:
        print("Inconclusive")
        return "Inconclusive"

def main(data):
    #load pickle files
    modelfilename = 'modelfile' 
    with open(modelfilename,'rb') as f:
        loaded_model = pickle.load(f)
        loaded_preprocessing = pickle.load(f)
        loaded_todrop = pickle.load(f)

    DROP_COLS = ['start','end']
    data = data.drop(DROP_COLS, axis = 1)
    df_data = preprocess(data, loaded_preprocessing, loaded_todrop)
    #preprocessed data, ready for model prediction

    resultVec = loaded_model.predict(df_data)
    print(resultVec)
    return finalCall(resultVec)

    
    
