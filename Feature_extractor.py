import parselmouth
from parselmouth.praat import call
import pandas as pd

def measurePitch(audio_file):
    sound = parselmouth.Sound(audio_file) # read the sound
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", 75, 300)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    return hnr, localJitter, localShimmer, 

# List to store data
data = []
# For Parkinson's Data
for i in range (1,16): #Customize to data set size
    audio_fileA = f"./Audioclips/HSet {i}A.wav"  # Replace with your actual file
    audio_fileB = f"./Audioclips/HSet {i}B.wav"
    featuresA = measurePitch(audio_fileA)    
    featuresB = measurePitch(audio_fileB)
    print(audio_fileA)
    print(featuresA)
    print(audio_fileB)
    print(featuresB)
    differences=[1,2,3]
    differences[0]=featuresB[0]-featuresA[0]
    differences[1]=featuresB[1]-featuresA[1]
    differences[2]=featuresB[2]-featuresA[2]
    print("Set",i,"difference")
    print(differences)
    data.append([differences[0], differences[1], differences[2], 0])

# For Healthy Data
for i in range (1,16): #Customize to data set size
    audio_fileA = f"./Audioclips/PSet {i}A.wav"  # Replace with your actual file
    audio_fileB = f"./Audioclips/PSet {i}B.wav"
    featuresA = measurePitch(audio_fileA)    
    featuresB = measurePitch(audio_fileB)
    print(audio_fileA)
    print(featuresA)
    print(audio_fileB)
    print(featuresB)
    differences=[1,2,3]
    differences[0]=featuresB[0]-featuresA[0]
    differences[1]=featuresB[1]-featuresA[1]
    differences[2]=featuresB[2]-featuresA[2]
    print("Set",i,"difference")
    print(differences)
    data.append([differences[0], differences[1], differences[2], 1])

#columns = ["HNR_Diff", "Jitter_Diff", "Shimmer_Diff", "Class"]
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv("differences_features.csv", index=False)

print("Data exported to pitch_features_labeled.csv")

