import pytest


# Фикстура для host (localhost)
@pytest.fixture
def host():
    return 'localhost'


# Фикстура для port (8080)
@pytest.fixture
def port():
    return 8080