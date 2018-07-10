#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tennisabstract` package."""

import pytest


from tennisabstract import tennisabstract
from tennisabstract import get_current_tournament


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')

def test_tournament():
    """Test tournament part"""
    list = get_current_tournament()
    assert len(list) >= 1
    

