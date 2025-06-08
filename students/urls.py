from django.urls import path
from . import views

urlpatterns = [
    path("ask/",
         views.ask_ai, 
         name="ask_ai"),
         
    path("generate-paper/",
         views.generate_paper_view,
         name="generate_paper"),

     
]