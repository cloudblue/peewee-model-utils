## Introduction to Ordered Model

In many cases of application development it is required to have order among the objects
od the same object and as an administrative operation, we would also like to have
different operation to arrange the object.

This can contain operations like:
1. Shifting an object after an object
2. Shifting an object before an object

Ordered model mixin provided this capability. The field position represents the 
position in ordered manner. Example:

``` python
from connect.utils.peewee.mixins import OrderedModelMixin, VerboseIDMixin
from tests.utils import db


class Item(VerboseIDMixin, OrderedModelMixin):
    @property
    def prefix(self):
        return 'TEST-ORD'

    name = peewee.CharField(null=True)

    class Meta:
        database = db


item1 = Item.create(name='E1')
item2 = Item.create(name='E2')
item3 = Item.create(name='E3')

print(item1.position)
10000
print(item2.position)
20000
print(item3.position)
30000

item3.sort(after=item1)

print(item1.position)
10000
print(item2.position)
30000
print(item3.position)
20000
```