import requests
import scipy.io.wavfile
import numpy as np

# Specify the audio file
file_name = 'audio.wav'
files = {'file': open(file_name, 'rb')}

# The parameter denoise_level is optional. If not set, the default value is 20.
denoise_level = 20
querystring = {"denoise_control": denoise_level}

# Only include 'x-rapidapi-key' in the header. 
headers = {
    'x-rapidapi-key': "your-rapidapi-key"
}

# RapidAPI url
url = "https://noise-reduction-service.p.rapidapi.com/denoise"

# Make API call
response = requests.request("POST", url, files=files, headers=headers, params=querystring)

# Convert byte data from response to audio format
content = np.frombuffer(response.content, dtype=np.int16)

# Save audio to the file with the original sample rate
sample_rate = 44100
scipy.io.wavfile.write('denoised_speech.wav', sample_rate, content)