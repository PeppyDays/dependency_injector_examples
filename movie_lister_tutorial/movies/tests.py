from unittest import mock

import pytest

from .containers import Container


@pytest.fixture
def container():
    container = Container(
        config={
            "finder": {
                "type": "memory",
                "csv": {
                    "path": "data/movies.csv",
                    "delimiter": ",",
                },
                "sqlite": {
                    "path": "data/movies.db",
                },
                "memory": {
                    "path": "data/movies.json",
                },
            },
        },
    )
    yield container


def test_movies_directed_by(container):
    finder_mock = mock.Mock()
    finder_mock.find_all.return_value = [
        container.movie("The 33", 2015, "Patricia Riggen"),
        container.movie("The Jungle Book", 2016, "Jon Favreau"),
    ]

    with container.finder.override(finder_mock):
        lister = container.lister()
        movies = lister.movies_directed_by("Jon Favreau")

    assert len(movies) == 1
    assert movies[0].title == "The Jungle Book"


def test_movies_released_in(container):
    finder_mock = mock.Mock()
    finder_mock.find_all.return_value = [
        container.movie("The 33", 2015, "Patricia Riggen"),
        container.movie("The Jungle Book", 2016, "Jon Favreau"),
    ]

    with container.finder.override(finder_mock):
        lister = container.lister()
        movies = lister.movies_released_in(2015)

    assert len(movies) == 1
    assert movies[0].title == "The 33"


def test_memory_db_works(container):
    finder = container.finder()
    movies = list(finder.find_all())

    assert len(movies) == 3
