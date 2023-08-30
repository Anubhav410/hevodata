from api.services.search.base import PostgresSearchBackend


def search_backend_factory(backend_name):
    if backend_name == "postgres":
        return PostgresSearchBackend()
    return PostgresSearchBackend()
