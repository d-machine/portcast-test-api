from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="get-routes"),
    path('get', views.fetch_new_paragraph, name="get-new-paragraph"),
    path('search', views.search_matching_paragraphs,
         name="get-matching-paragraphs"),
    path('dictionary', views.dictionary_top_10, name='get-meaning-of-top-10')
]
