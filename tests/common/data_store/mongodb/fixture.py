# coding: utf-8
import pytest
from nmp_broker import create_app


@pytest.fixture(scope="module")
def app():
    app = create_app()
    yield app