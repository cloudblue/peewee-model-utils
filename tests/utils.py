import functools

import peewee


db = peewee.SqliteDatabase(':memory:')


def use_test_database(
        func=None,
        models=None,
):
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            db.create_tables(models)
            try:
                func(*args, **kwargs)
            finally:
                db.drop_tables(models)

        return wrapper

    return inner(func) if callable(func) else inner
