
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *  
 
urlpatterns = [       
     
    path('', dashboard, name='dashboard'), 
    path('getResults/', getResults, name='getResults'), 
    path('genrateQuestionView/', genrateQuestionView, name='genrateQuestionView'), 
    
    
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

