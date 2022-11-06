import tempfile
import shutil

from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

get_paragraph_url = reverse('get-new-paragraph')
search_paragraph_url = reverse('get-matching-paragraphs')
dictionary_url = reverse('get-meaning-of-top-10')


def search_paragraph_url(keywords, operator):
    base_url = reverse('get-matching-paragraphs')

    return '%s?%s' % (base_url, urlencode({'keywords': keywords, 'operator': operator}))


class PortcastApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.fetch_paragraph_patcher = patch(
            'portcast.api.views.fetch_a_paragraph')

        self.fetch_a_paragraph = self.fetch_paragraph_patcher.start()
        self.fetch_a_paragraph.return_value = 'This is test paragraph'
        self.fetch_meaning_patcher = patch(
            'portcast.api.views.fetch_meaning')
        self.fetch_meaning = self.fetch_meaning_patcher.start()
        self.fetch_meaning.return_value = {'meaning': 'some_meaning'}
        self.test_dir = tempfile.mkdtemp()
        self.addClassCleanup(self.fetch_paragraph_patcher.stop)
        self.addClassCleanup(self.fetch_meaning_patcher.stop)

    def test_fetch_new_paragraph(self):
        with self.settings(MEDIA_ROOT=self.test_dir):
            res = self.client.get(get_paragraph_url)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, 'This is test paragraph')

    def test_search_matching_paragraphs(self):
        with self.settings(MEDIA_ROOT=self.test_dir):
            res = self.client.get(get_paragraph_url)
            res = self.client.get(search_paragraph_url('This,is', 'and'))

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, ['This is test paragraph'])

    def test_dictionary_top_10(self):
        with self.settings(MEDIA_ROOT=self.test_dir):
            res = self.client.get(get_paragraph_url)
            res = self.client.get(dictionary_url)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, {
                'This': {'meaning': 'some_meaning'},
                'is': {'meaning': 'some_meaning'},
                'test': {'meaning': 'some_meaning'},
                'paragraph': {'meaning': 'some_meaning'}
            })

    def tearDown(self):
        shutil.rmtree(self.test_dir)
