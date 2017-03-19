# -*- coding: utf-8 -*-

""" Provides index creation and search functions for GeoLite2 city data """

import os
import csv
import unicodedata
import shutil
from operator import itemgetter

from tqdm import tqdm
from whoosh.index import create_in, open_dir
from whoosh.fields import SchemaClass, TEXT, STORED
from whoosh.qparser import QueryParser, FuzzyTermPlugin
from whoosh.query import Prefix
from whoosh.analysis import NgramWordAnalyzer


DATA_BASE_DIR = 'data'
CITY_DATA_FILE = 'GeoLite2-City-Locations-en.csv'

INDEX_BASE_DIR = 'index'
CITY_INDEX = 'city'


def current_path():
    """ Returns the absolute directory of this file """

    return os.path.dirname(os.path.abspath(__file__))


def index_path(index_name):
    """ Returns the absolute index path for the given index name """

    index_dir = '{}_index'.format(index_name)
    return os.path.join(current_path(), INDEX_BASE_DIR, index_dir)


def data_file_path(file_name):
    """ Returns the absolute path to the data file with the given name """

    return os.path.join(current_path(), DATA_BASE_DIR, file_name)


class CitySchema(SchemaClass):
    """ Whoosh schema for city search index """

    city = TEXT(stored=True)
    state = TEXT(stored=True)
    country = TEXT(stored=True)
    content = TEXT(analyzer=NgramWordAnalyzer(minsize=2), phrase=False)


def create_index():
    """ Create search index files """

    path = index_path(CITY_INDEX)

    if os.path.exists(path):
        shutil.rmtree(path)

    os.makedirs(path)

    index = create_in(path, CitySchema)
    writer = index.writer()

    with open(data_file_path(CITY_DATA_FILE)) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in tqdm(reader, desc='Creating city index'):
            city = row.get('city_name')

            if city:
                state = row.get('subdivision_1_name')
                country = row.get('country_name')
                content = _cleanup_text(' '.join([city, state, country]))

                writer.add_document(
                    city=city,
                    state=state,
                    country=country,
                    content=content
                )

        print('Committing data...', end='')
        writer.commit()
        print('done')

    return True


def search(query='', count=10):
    """ Searches for the given city """

    index = open_dir(index_path(CITY_INDEX))

    with index.searcher() as searcher:
        parser = QueryParser('content', index.schema, termclass=Prefix)
        parsed_query = parser.parse(query)
        results = searcher.search(parsed_query, limit=count)

        data = [[result['city'],
                 result['state'],
                 result['country']]
                for result in results]

        return data


def _cleanup_text(text):
    """ Removes accents and replaces umlauts """

    replaces = [
        ['ä', 'ae'],
        ['ö', 'oe'],
        ['ü', 'ue'],
        ['Ä', 'Ae'],
        ['Ö', 'Oe'],
        ['Ü', 'Ue'],
        ['ß', 'ss']
    ]

    for original, replacement in replaces:
        text = text.replace(original, replacement)

    text = unicodedata.normalize('NFKD', text)
    text = ''.join([char for char in text if not unicodedata.combining(char)])
    text = text.encode('ascii', 'ignore').decode('ascii')

    return text
