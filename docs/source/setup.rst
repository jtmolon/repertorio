Setup
=====

Prerequisites
-------------

Repertorio works on Python 3.7+, and has the `requests <https://requests.kennethreitz.org/en/master/>`_ library as its sole dependency. It will be installed automatically, so nothing to worry about.

To play around with the `setlist.fm <https://www.setlist.fm/>`_ API you'll need an API access key. You can easily get one `here <https://www.setlist.fm/signin>`_

Installation
------------

If you're using `pipenv <https://pipenv.readthedocs.io/en/latest/>`_ to manage your dependencies::

  $ pipenv install repertorio

Otherwise, if you're using pip::

  $ pip install repertorio

Basic usage
-----------
::

  from repertorio import Repertorio
  api = Repertorio('setlistfm-api-key')
