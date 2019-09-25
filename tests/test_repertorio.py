# -*- coding: utf-8 -*-

"""Tests for repertorio package"""

import json
import os
from unittest import mock

import pytest
from requests.exceptions import HTTPError, Timeout, TooManyRedirects

from repertorio import Repertorio
from repertorio.repertorio import (
    MissingPKForResource,
    MissingSearchCriteria,
    SEARCH,
    RESOURCE,
)


DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@pytest.fixture(scope="module")
def api():
    """Returns Repertorio object"""
    return Repertorio("api-key")


@pytest.fixture()
def json_data():
    """"""

    def _json_data(endpoint):
        with open(f"{DATA_DIR}/{endpoint}.json") as file:
            return json.loads(file.read())

    return _json_data


def test___getattr__attr_error(api):
    """Tests __getattr__ for api raises AttributeError on invalid endpoint"""
    with pytest.raises(AttributeError):
        api.invalid_endpoint()


def test__validate_request_missing_search_criteria(api):
    """Tests _validate_request for api raises MissingSearchCriteria on missing kwargs"""
    for endpoint in SEARCH.values():
        if endpoint == "search/countries":
            continue
        with pytest.raises(MissingSearchCriteria):
            api._validate_request(endpoint)


def test__validate_request_missing_pk(api):
    """Tests _validate_request for api raises MissingSearchCriteria on missing pk argument"""
    for endpoint in RESOURCE.values():
        with pytest.raises(MissingPKForResource):
            api._validate_request(endpoint)


def test__resource_search(api, json_data):
    api_get_mock = mock.Mock()
    api_get_mock.return_value.json.return_value = json_data("artists")
    api.session.get = api_get_mock
    expected = json_data("artists")
    actual = api.artists(artistName="chain", sort="relevance")
    assert json.dumps(expected) == json.dumps(actual)


def test__resource_pk(api, json_data):
    api_get_mock = mock.Mock()
    api_get_mock.return_value.json.return_value = json_data("artist")
    api.session.get = api_get_mock
    expected = json_data("artist")
    actual = api.artist("4bd95eea-b9f6-4d70-a36c-cfea77431553")
    assert json.dumps(expected) == json.dumps(actual)


def test__resource_timeout(api, json_data):
    api_get_mock = mock.Mock()
    api_get_mock.side_effect = Timeout()
    api.session.get = api_get_mock
    with pytest.raises(Timeout):
        api.artists(artistName="foo")


def test__resource_too_many_redirects(api, json_data):
    api_get_mock = mock.Mock()
    api_get_mock.side_effect = TooManyRedirects()
    api.session.get = api_get_mock
    with pytest.raises(TooManyRedirects):
        api.artists(artistName="foo")


def test__resource_http_error(api, json_data):
    api_get_mock = mock.Mock()
    api_get_mock.return_value.raise_for_status.side_effect = HTTPError()
    api.session.get = api_get_mock
    with pytest.raises(HTTPError):
        api.artists(artistName="foo")


def test__resource_value_error(api, json_data):
    api_get_mock = mock.Mock()
    api_get_mock.return_value.json.side_effect = ValueError()
    api.session.get = api_get_mock
    with pytest.raises(ValueError):
        api.artists(artistName="foo")
