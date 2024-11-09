import requests
import json

def emotion_detector(text_to_analyze):
    URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    response = requests.post(URL, json = input_json, headers=header)
    formated_response = json.loads(response.text)
    if response.status_code == 200:
        formatted_response = json.loads(response.text)
    elif response.status_code == 500:
        formatted_response = {
        return formated_response
    elif response.status_code == 400:
        formated_response = {
                            'anger': None,
                            'disgust': None, 
                            'fear': None, 
                            'joy': None, 
                            'sadness': None, 
                            'dominant_emotion': None}
    return formatted_response
        return formated_response

def emotion_predictor(detected_text):
    emotions = detected_text['emotionPredictions'][0]['emotion']
    anger = emotions['anger']
    disgust = emotions['disgust']
    fear = emotions['fear']
    joy = emotions['joy']
    sadness = emotions['sadness']
    max_emotion = max(emotions, key=emotions.get)
    #max_emotion_score = emotions[max_emotion]
    formated_dict_emotions = {
                            'anger': anger,
                            'disgust': disgust,
                            'fear': fear,
                            'joy': joy,
                            'sadness': sadness,
                            'dominant_emotion': max_emotion
                            }
    return formated_dict_emotions
    if all(value is None for value in detected_text.values()):
        return detected_text
    if detected_text['emotionPredictions'] is not None:
        emotions = detected_text['emotionPredictions'][0]['emotion']
        anger = emotions['anger']
        disgust = emotions['disgust']
        fear = emotions['fear']
        joy = emotions['joy']
        sadness = emotions['sadness']
        max_emotion = max(emotions, key=emotions.get)
        #max_emotion_score = emotions[max_emotion]
        formated_dict_emotions = {
                                'anger': anger,
                                'disgust': disgust,
                                'fear': fear,
                                'joy': joy,
                                'sadness': sadness,
                                'dominant_emotion': max_emotion
                                }
        return formated_dict_emotions
‎server.py
+26
-4
Original file line number	Diff line number	Diff line change
@@ -1,17 +1,39 @@
"""
Emotion Detection Server
This script defines a Flask-based server for performing emotion detection on user-provided text.
Author(Learner): [NoorAldin]
"""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector
from EmotionDetection.emotion_detection import emotion_predictor

app = Flask("Emotion Detection")

def run_emotion_detection():
    """
    Main function to run the Emotion Detection application.
    """
    app.run(host="0.0.0.0", port=5000)
@app.route("/emotionDetector")
def sent_detector():
    """
    Analyze the user-provided text for emotions and return the result.
    """
    text_to_detect = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_detect)
    formated_response = emotion_predictor(response)
    if formated_response['dominant_emotion'] == None:
        return "Invalid text! Please try again!."
    return f"For the given statement, the system response is 'anger': {formated_response['anger']} 'disgust': {formated_response['disgust']}, 'fear': {formated_response['fear']}, 'joy': {formated_response['joy']} and 'sadness': {formated_response['sadness']}. The dominant emotion is {formated_response['dominant_emotion']}."
    if formated_response['dominant_emotion'] is None:
        return "Invalid text! Please try again."
    return (
        f"For the given statement, the system response is 'anger': {formated_response['anger']} "
        f"'disgust': {formated_response['disgust']}, 'fear': {formated_response['fear']}, "
        f"'joy': {formated_response['joy']} and 'sadness': {formated_response['sadness']}. "
        f"The dominant emotion is {formated_response['dominant_emotion']}."
    )

@app.route("/")
def render_index_page():
@@ -21,4 +43,4 @@ def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    run_emotion_detection()
0 commit comments
Comments
0
