# import pytest
# from app import app


# @pytest.fixture(scope='module')
# def test_app():
#     return app.test_client()

import pytest
from app import app

@pytest.fixture(scope="module")
def test_client():
    with app.app_context():
        yield app.test_client()
        