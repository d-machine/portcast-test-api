
import os

from django.conf import settings
from functools import partial
from multiprocessing import Pool
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import WordFrequency
from .utils import (fetch_a_paragraph, write_paragraph_to_file,
                    update_frequency, match_files, fetch_meaning)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/get',
        '/api/search',
        '/api/dictionary'
    ]
    return Response(routes)


@api_view(['GET'])
def fetch_new_paragraph(request):
    """Fetch, store and return a new paragraph"""
    paragraph = fetch_a_paragraph()
    write_paragraph_to_file(paragraph)
    update_frequency(paragraph)

    return Response(paragraph)


@api_view(['GET'])
def search_matching_paragraphs(request):
    """Returns paragraphs matching the search"""
    query_params = request.query_params

    keywords = query_params.get('keywords', '').split(',')
    keywords = [x.strip() for x in keywords]

    operator = request.query_params.get('operator', None)

    print(query_params)
    print(keywords, operator)

    if operator not in ['or', 'and']:
        return Response(
            'Operator must be one of "or" or "and"',
            status=status.HTTP_400_BAD_REQUEST
        )

    all_files = os.listdir(settings.MEDIA_ROOT)
    print(all_files)
    pool = Pool()

    results = pool.map(partial(match_files, keywords, operator), all_files)

    results = [x for x in results if x]

    return Response(results)


@api_view(['GET'])
def dictionary_top_10(request):
    """Return top 10 words in dictionary"""
    result = {}
    top10_objects = WordFrequency.objects.all().values()
    if len(top10_objects) > 10:
        top10_objects[:10]

    for row in top10_objects:
        word = row['word']

        result[word] = fetch_meaning(word)

    return Response(result)
