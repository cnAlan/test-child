# coding: utf-8
import pytest
from nmp_broker import create_app


@pytest.fixture(scope="module")
def app():
    app = create_app()
    yield app


@pytest.fixture(scope="module")
def client():
    app = create_app()
    client = app.test_client()
    yield client