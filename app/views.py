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

# Create your views here.


def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary


def loginRouter(request):  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password) 
        if user is not None:
            login(request, user) 
            return redirect('dashboard')
        else: 
            return redirect('loginRouter')
 
    return render(request, 'app/login.html' ) 


def logoutRouter(request):    
    logout(request)
    return redirect('loginRouter')


# @login_required(login_url="/login/")
def dashboard(request):     
    return render(request, 'app/dashboard.html' ) 

# @login_required(login_url="/login/")
def getResults(request):  
    context = {}  
    video_id = request.GET['video_id']
    scale = float(str(request.GET['scale']))
    print(video_id) 
    print("-> Getting Subtitle")
    
    subtitle = YouTubeTranscriptApi.get_transcript("Cgxsv1riJhI") 
    subtitle = " ".join( [x['text'] for x in subtitle]).strip()

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,la;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryC4Vpis0XcgA73e3A',
        'Origin': 'http://bark.phon.ioc.ee',
        'Referer': 'http://bark.phon.ioc.ee/punctuator',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    data = f'------WebKitFormBoundaryC4Vpis0XcgA73e3A\r\nContent-Disposition: form-data; name="text"\r\n\r\n{subtitle}\r\n------WebKitFormBoundaryC4Vpis0XcgA73e3A--\r\n'
    print("-> Getting Punctuation")
    punctuated_subtitle = requests.post('http://bark.phon.ioc.ee/punctuator', headers=headers, data=data, verify=False) 
    punctuated_subtitle = str(punctuated_subtitle.text).strip()
    context['punctuated_subtitle'] = punctuated_subtitle
    context['summarized_subtitle'] = "N/A"
    
    print("-> Getting Summary")
    try:
        context['summarized_subtitle'] = summarize(punctuated_subtitle, scale)
    except:
        pass




    return JsonResponse(context)