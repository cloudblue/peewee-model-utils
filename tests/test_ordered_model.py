import peewee
import pytest

from connect.utils.peewee.mixins import OrderedModelMixin, VerboseIDMixin
from tests.utils import db


class OrderedTestModel(VerboseIDMixin, OrderedModelMixin):
    @property
    def prefix(self):
        return 'TEST-ORD'

    name = peewee.CharField(null=True)

    class Meta:
        database = db


def refresh_objects(model, objs):
    if type(objs) != list:
        objs = [objs]

    return [model.get(obj._pk_expr()) for obj in objs]


@pytest.mark.provide_objects(model=OrderedTestModel, count=3)
def test_default_position_value(obj0, obj1, obj2):

    assert obj0.position == 10000
    assert obj1.position == 20000
    assert obj2.position == 30000


@pytest.mark.provide_objects(model=OrderedTestModel, count=3)
def test_sort_after(obj0, obj1, obj2):

    obj2.sort(after=obj0)

    objs = refresh_objects(OrderedTestModel, [obj0, obj1, obj2])

    assert [obj.position for obj in objs] == [10000, 30000, 20000]


@pytest.mark.provide_objects(model=OrderedTestModel, count=3)
def test_sort_before(obj0, obj1, obj2):

    obj2.sort(before=obj1)

    objs = refresh_objects(OrderedTestModel, [obj0, obj1, obj2])

    assert [obj.position for obj in objs] == [10000, 30000, 20000]


@pytest.mark.provide_objects(model=OrderedTestModel, count=4)
def test_sort_before_from_top(obj0, obj1, obj2, obj3):

    obj1.sort(before=obj3)

    objs = refresh_objects(OrderedTestModel, [obj0, obj1, obj2, obj3])

    assert [obj.position for obj in objs] == [10000, 30000, 20000, 40000]


@pytest.mark.provide_objects(model=OrderedTestModel)
def test_sort_after_with_same(obj0):
    with pytest.raises(ValueError):
        obj0.sort(after=obj0)


@pytest.mark.provide_objects(model=OrderedTestModel, count=2)
def test_sort_before_with_same_position_value(obj0, obj1):
    obj1.position = obj0.position
    obj1.save()

    with pytest.raises(ValueError):
        obj0.sort(before=obj1)


@pytest.mark.provide_objects(model=OrderedTestModel, count=4)
def test_sort_place_at_top(obj0, obj1, obj2, obj3):

    obj2.sort()

    objs = refresh_objects(OrderedTestModel, [obj0, obj1, obj2, obj3])

    assert [obj.position for obj in objs] == [20000, 30000, 10000, 40000]


@pytest.mark.provide_objects(model=OrderedTestModel, count=4)
def test_sort_after_from_in_between(obj0, obj1, obj2, obj3):

    obj1.sort(after=obj2)

    objs = refresh_objects(OrderedTestModel, [obj0, obj1, obj2, obj3])

    assert [obj.position for obj in objs] == [10000, 30000, 20000, 40000]


@pytest.mark.provide_objects(model=OrderedTestModel, count=4)
def test_sort_after_no_element_in_between(obj0, obj1, obj2, obj3):

    obj2.sort(after=obj1)

    objs = refresh_objects(OrderedTestModel, [obj0, obj1, obj2, obj3])

    assert [obj.position for obj in objs] == [10000, 20000, 30000, 40000]
