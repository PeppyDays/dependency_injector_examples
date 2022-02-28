from dependency_injector import containers
from dependency_injector import providers

from . import entities
from . import finders
from . import listers


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yaml"])
    movie = providers.Factory(entities.Movie)

    csv_finder = providers.Singleton(
        finders.CsvMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.csv.path,
        delimiter=config.finder.csv.delimiter,
    )

    sqlite_finder = providers.Singleton(
        finders.SqliteMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.sqlite.path,
    )

    memory_finder = providers.Singleton(
        finders.MemoryMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.memory.path,
    )

    finder = providers.Selector(
        config.finder.type,
        csv=csv_finder,
        sqlite=sqlite_finder,
        memory=memory_finder,
    )

    lister = providers.Factory(
        listers.MovieLister,
        movie_finder=finder,
    )
