import csv
import json
import sqlite3
from sqlite3 import Connection
from typing import Callable

from .entities import Movie


class MovieFinder:
    _movie_factory: Callable[..., Movie]

    def __init__(self, movie_factory: Callable[..., Movie]):
        self._movie_factory = movie_factory

    def find_all(self) -> list[Movie]:
        raise NotImplementedError


class CsvMovieFinder(MovieFinder):
    _movie_factory: Callable[..., Movie]
    _csv_file_path: str
    _delimiter: str

    def __init__(self, movie_factory: Callable[..., Movie], path: str, delimiter: str):
        super().__init__(movie_factory)
        self._csv_file_path = path
        self._delimiter = delimiter

    def find_all(self) -> list[Movie]:
        with open(self._csv_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self._delimiter)

            for row in csv_reader:
                title, year, director = row
                yield self._movie_factory(title, int(year), director)


class SqliteMovieFinder(MovieFinder):
    _movie_factory: Callable[..., Movie]
    _database: Connection

    def __init__(self, movie_factory: Callable[..., Movie], path: str):
        self._database = sqlite3.connect(path)
        super().__init__(movie_factory)

    def find_all(self) -> list[Movie]:
        with self._database as db:
            rows = db.execute("select title, year, director from movies")
            for row in rows:
                title, year, director = row
                yield self._movie_factory(title, int(year), director)


class MemoryMovieFinder(MovieFinder):
    _movie_factory: Callable[..., Movie]
    _records: list[dict]

    def __init__(self, movie_factory: Callable[..., Movie], path: str):
        super().__init__(movie_factory)
        self._records = json.loads(open(path, "r").read())

    def find_all(self) -> list[Movie]:
        for record in self._records:
            yield self._movie_factory(**record)
