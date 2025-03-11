# Overview
Parkinson's Disease (PD), a neurodegenerative disorder, affects millions around the world. Early recognition and diagnosis of PD is crucial to getting the proper treatment and early intervention. According to the Cleveland Clinic, between 75% and 90% of patients develop dysarthria and voice problem, which may include a reduction in volume, slurring, mumbling, monotone pitch, and breathiness or hoarseness in the voice. A study has shown that early patterns of dysarthria are detectable up to 10 years before diagnosis. There are existing studies of PD detection via speech analysis, but they lack prodromal recordings. Since PD is a progressive disease, it would be effective to monitor the changes in speech characteristics over a period of time. A machine learning model that could detect PD based on longitudinal speech data was developed. 

# Program Components
**Youtubetoaudio.py** - Extracts audio and converts them into WAV files when given a public YouTube link and specified a time segment. Background noise is removed. 

**Feature_extractor.py** - Takes the audio files and extracts jitter, shimmer, and harmonics-to-noise ratio from each one. Based on the files given, this program will find the differences of the features for the each set. Converts complete data set to CSV file.

**mlmodels.ipynb** - Program that trains 3 machine-learning algorithms based on the data set provided: Support Vector Machines, Logistic Regression, and Random Forest
