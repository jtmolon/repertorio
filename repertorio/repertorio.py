# -*- coding: utf-8 -*-

"""A setlist.fm API wrapper"""
import logging
from typing import Any, Callable, Dict, Optional

import requests
from requests.exceptions import HTTPError, Timeout, TooManyRedirects

logger: logging.Logger = logging.getLogger(__name__)

SEARCH: Dict[str, str] = {
    "artists": "search/artists",
    "cities": "search/cities",
    "countries": "search/countries",
    "setlists": "search/setlists",
    "venues": "search/venues",
}

RESOURCE: Dict[str, str] = {
    "artist": "artist/{pk}",
    "artist_setlists": "artist/{pk}/setlists",
    "city": "city/{pk}",
    "setlist": "setlist/{pk}",
    "setlist_version": "setlist/version/{pk}",
    "user": "user/{pk}",
    "user_attended": "user/{pk}/attended",
    "user_edited": "user/{pk}/edited",
    "venue": "venue/{pk}",
    "venue_setlists": "venue/{pk}/setlists",
}


class MissingSearchCriteria(ValueError):
    """Exception raised on missing search criteria"""

    pass


class MissingPKForResource(TypeError):
    """Exception on missing primary key argument"""

    pass


class Repertorio:
    """setlist.fm API wrapper class"""

    def __init__(self, api_key: str) -> None:
        """Constructs the API wrapper object.

        :param api_key: The API access key
        :type api_key: str
        """
        self.api_key: str = api_key
        self.url: str = "https://api.setlist.fm/rest/1.0/"
        self.headers: Dict[str, str] = {
            "x-api-key": api_key,
            "Accept": "application/json",
        }
        self.session: requests.Session = requests.Session()

    def __getattr__(self, attr: str) -> Callable[[Any, Any], Any]:
        """Endpoint wrapper

        :param attr: endpoint identifier
        :type attr: str
        :raises AttributeError if attr can't be found in SEARCH or RESOURCE
        :returns: A callable, if attr can be found in SEARCH or RESOURCE
        :rtype: callable
        """
        if attr in SEARCH:

            def search(*args: Any, **kwargs: Any) -> Callable[[Any, Any], Any]:
                return self._resource(SEARCH[attr], *args, **kwargs)

            return search

        if attr in RESOURCE:

            def resource(*args: Any, **kwargs: Any) -> Callable[[Any, Any], Any]:
                return self._resource(RESOURCE[attr], *args, **kwargs)

            return resource

        raise AttributeError

    def _validate_request(
        self, endpoint: str, pk: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Validates endpoint request based on the type of resource being requested
        :param endpoint: resource endpoint identifier
        :type attr: str
        :param pk: resource primary key
        :type pk: str
        :param args: positional arguments passed into the function
        :type args: Tuple
        :param kwargs: keyword arguments passed into the function, representing query string parameters for request
        :type kwargs: dict
        :raises MissingPKForResource if no pk is provided for a RESOURCE endpoint
        :raises MissingSearchCriteria if no search criteria is provided for a SEARCH endpoint
        """
        if (
            endpoint in SEARCH.values()
            and endpoint != "search/countries"
            and not kwargs
        ):
            raise MissingSearchCriteria(kwargs)
        if endpoint in RESOURCE.values() and not pk:
            raise MissingPKForResource(endpoint)

    def _resource(self, endpoint: str, pk: Optional[str] = None, **kwargs: Any) -> Any:
        """Get specific resource from an endpoint, given it's primary key

        :param endpoint: resource endpoint identifier
        :type attr: str
        :param pk: resource primary key
        :type pk: str
        :param args: positional arguments passed into the function
        :type args: Tuple
        :param kwargs: keyword arguments passed into the function, representing query string parameters for request
        :type kwargs: dict
        :returns: Request JSON response content or None in case of failure
        :rtype: Any
        """
        self._validate_request(endpoint, pk, **kwargs)
        request_kwargs: Dict[str, Any] = (
            {"url": f"{self.url}{endpoint}".format(pk=pk)}
            if pk
            else {"url": f"{self.url}{endpoint}"}
        )
        request_kwargs["params"] = kwargs
        return self._get(request_kwargs)

    def _get(self, kwargs: Dict[str, Any]) -> Any:
        """Performs GET request to API

        :param kwargs: keyword arguments passed into the function, representing query string parameters for request
        :type kwargs: dict
        :raises Timeout if the request times out.
        :raises TooManyRedirects if the request has too many redirects to follow.
        :raises ValueError if the resulting JSON response is invalid.
        :raises HTTPError if the response status code is bad.
        :returns: Request JSON response content or None in case of failure
        :rtype: Any
        """
        try:
            kwargs["headers"] = self.headers
            response = self.session.get(**kwargs)
        except Timeout:
            logger.error("Request timed out")
            raise
        except TooManyRedirects:
            logger.error("Request had too many redirects")
            raise
        finally:
            self.session.close()

        try:
            response.raise_for_status()
            try:
                response_json = response.json()
            except ValueError:
                logger.error("Invalid response format")
                raise
            else:
                return response_json
        except HTTPError as e:
            logger.error(f"HTTP exception: {repr(e)}")
            raise
