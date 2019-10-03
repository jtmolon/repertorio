Usage
=====

::

  from repertorio import Repertorio
  api = Repertorio('setlistfm-api-key')
  api.artists(artistName='alice', sort='relevance')


Search endpoints
----------------

The API search endpoints return multiple results, in case of match, and require keyword arguments to perform the query. Refer to the `API documentation <https://api.setlist.fm/docs/1.0/index.html>`_ for details of supported keyword arguments and response formats

::

    api.artists(artistName='foo')
    api.cities(name='caxias do sul')
    api.countries()  # countries is an exception, it doesn't require or support any keyword arguments
    api.setlists(artistName='foo')
    api.venues(name='olympia theatre')


Resource endpoints
------------------

The API resource endpoints return a single result and, as such, require a "primary key" argument to perform the query. Refer to the `API documentation <https://api.setlist.fm/docs/1.0/index.html>`_ for further details

::

    api.artist('artist-mbid')
    api.artist_setlists('artist-mbid')
    api.city('city-geoId')
    api.setlist('setlistId')
    api.setlist_version('versionId')
    api.user('userId')
    api.user_attended('userId')
    api.user_edited('userId')
    api.venue('venueId')
    api.venue_setlists('venueId')
