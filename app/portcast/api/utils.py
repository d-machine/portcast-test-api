import re
import time
import requests

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import WordFrequency


def fetch_a_paragraph():
    """Function to fetch and return a paragraph"""
    api_url = "http://metaphorpsum.com/paragraphs/1/50"
    response = requests.get(api_url)
    return response.content.decode("utf-8")


def write_paragraph_to_file(paragraph):
    """Function to write paragraph to filesystem"""
    fs = FileSystemStorage()

    curr_time = int(str(time.time()).replace('.', ''))

    with fs.open('{}.txt'.format(curr_time), 'w') as fh:
        fh.write(paragraph)


def update_frequency(paragraph):
    all_words = (re.findall(r'\w+', paragraph))

    all_words_count_dict = {}

    for word in all_words:
        if word not in all_words_count_dict:
            all_words_count_dict[word] = 0
        all_words_count_dict[word] += 1

    for word in all_words_count_dict:
        try:
            obj = WordFrequency.objects.get(word=word)
            obj.frequency += all_words_count_dict[word]
            obj.save()
        except:
            obj = WordFrequency(
                word=word, frequency=all_words_count_dict[word])
            obj.save()


def match_files(keywords, operator, filename):
    print(filename, keywords, operator)
    filepath = '%s/%s' % (settings.MEDIA_ROOT, filename)

    paragraph = ''

    with open(filepath, 'r') as fh:
        paragraph = fh.read()

    all_words = set(re.findall(r'\w+', paragraph))

    operation = any if operator == 'or' else all

    is_match = operation(word in all_words for word in keywords)

    if is_match:
        return paragraph

    return False


def fetch_meaning(word):
    api_url_template = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"
    api_url = api_url_template.format(word)

    return requests.get(api_url).json()
