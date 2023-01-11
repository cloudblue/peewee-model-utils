import pytest
from _pytest.fixtures import FixtureDef, SubRequest

from tests.utils import db


@pytest.fixture(autouse=True, scope='function')
def add_fixture_dynamically(request: SubRequest):
    """
    Conditionally and dynamically adds Peewee Model objects as fixture.
    It's conditional on the presence of:

        @pytest.mark.provide_objects(prefix, model, count)

        Where:
            prefix: Fixture prefix. Default value is 'obj'.
            model: Peewee model for which you want the objects
            count: Number of objects to be created. Default value is 1.
    """
    marker = request.node.get_closest_marker('provide_objects')
    model = None

    # don't register fixture if marker is not present:
    if marker and marker.kwargs['model']:
        model = marker.kwargs['model']

        count = 1 if 'count' not in marker.kwargs else (marker.kwargs['count'] or 1)
        prefix = 'obj' if 'prefix' not in marker.kwargs else (marker.kwargs['prefix'] or 'obj')

        def fixture_func():
            if not db.table_exists(model.__name__.lower()):
                db.create_tables([model])
            return model.create()

        # register the fixture just-in-time
        for _ in range(count):

            request._fixturemanager._arg2fixturedefs[f'{prefix}{_}'] = [
                FixtureDef(
                    argname=f'{prefix}{_}',
                    func=fixture_func,
                    scope="function",
                    fixturemanager=request._fixturemanager,
                    baseid=None,
                    params=None,
                ),
            ]

    yield
    if model:
        db.drop_tables([model])
