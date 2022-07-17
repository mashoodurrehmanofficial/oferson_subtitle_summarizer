from django.http.response import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import nltk
nltk.download('stopwords')
from Questgen import main
 
payload_text = str(input("Enter payload = ")) 
input_question = str(input("Enter input question = ")) 
question_type = str(input("Enter question type = ")) 

print("question_type = ", question_type)
payload = {"input_text": str(payload_text)}

print("-> Generating Output")

if question_type=='True/False':
    qe= main.BoolQGen()
    output = qe.predict_boolq(payload)
    print (output)
    
    
elif question_type=='MCQs':
    qg = main.QGen()
    output = qg.predict_mcq(payload)
    print (output)
    
    
    
elif question_type=='FAQ':
    qg = main.QGen()    
    output = qg.predict_shortq(payload)
    print (output)
    
    
elif question_type=='Ask Question':
    payload = {"input_text": str(payload_text),"input_question":input_question}
    answer = main.AnswerPredictor()
    output = answer.predict_answer(payload)
    print (output)


