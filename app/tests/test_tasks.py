import pytest

from app.celery.tasks import generate_candidates_csv_file


@pytest.fixture(scope="module")
def celery_app():
    from celery import Celery

    test_celery_app = Celery(broker="redis://localhost:6379/0")
    return test_celery_app


def test_generate_candidates_csv_file(celery_app):
    """
    Test generation of a CSV file for candidates.
    """
    file_path = generate_candidates_csv_file()

    assert "candidates__" in file_path
