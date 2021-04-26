##Opensmile Feature Extraction
import pandas as pd
import opensmile
import csv
import librosa
from math import floor
from sox import file_info
import time
#DATA_FOLDER = '/Users/johnheo/medesign/neurologue.ai/audiodata/'
#function to extract audio features from audio file
def OpenSmileAnalysis(file):
    global period
    period = 2 #2 second windows
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
        store.append(SegmentAnalysis(signal,sr,i))
    return store

#function to extract audio features from slice within audio file
def SegmentAnalysis(signal,sr,i):
    GMAPsmile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.GeMAPSv01b,
        feature_level=opensmile.FeatureLevel.Functionals,
        num_channels = 1)
    y = GMAPsmile.process_signal(signal,sampling_rate=sr,start=pd.Timedelta(i*1000000000*period),end=pd.Timedelta((i+1)*1000000000*period))
    y = y.reset_index()
    return y


def main(file):
    store = [] #contain extracted data
    file = 'audio.wav'
    print("Beginning audio extraction....")
    starttime = time.perf_counter()
    for item in OpenSmileAnalysis(file):
        store.append(item)
    data = store[0]
    for item in store[1:]:
        data = data.append(item)
    print(f"Finished feature extraction in {time.perf_counter()-starttime:0.2f} seconds")
    #print(data.head())
    return data
"""
if __name__ == "__main__":
    #INIT VARIABLES
    period = 2 #2 second windows
    store = [] #contain extracted data
    file = 'audio.wav'

    #begin Audio Extraction
    print("Beginning audio extraction....")
    starttime = time.perf_counter()
    df_feature = Extract(file)
    print(f"Finished feature extraction in {time.perf_counter()-starttime:0.2f} seconds")
    print(df_feature.head())
    #print performance time
"""