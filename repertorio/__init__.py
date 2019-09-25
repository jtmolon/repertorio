# -*- coding: utf-8 -*-

"""A setlist.fm API wrapper"""
import itertools as it

from .repertorio import Repertorio, SEARCH, RESOURCE

endpoints = tuple(it.chain(SEARCH.keys(), RESOURCE.keys()))

__author__ = "Joao Molon"
__email__ = "<jtmolon@gmail.com>"
__version__ = "0.0.1"
__all__ = ["Repertorio", "endpoints"]
