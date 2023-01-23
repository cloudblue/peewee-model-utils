## Introduction to Transactional Verbose ID

Recommended Reading
[Verbose ID](verbose_id.md)

Transactional Verbose ID is useful when you have a base object with [Verbose ID](verbose_id.md)
and there are child objects belongs to that base object. In this case, there should a way to
identify the base object based on the ID of the client object. Child object ID can have
its own prefix, but it should inherit the digits from the parent object ID and as there can be
a number of children belong to the same base object, so the ID should be suffixed with 
a serial number indicating the position of that child object on creation time.

The best example will be the relationship between Product and Item. Here Products are the base 
objects and Items are the child objects belonging to base. You can´t have Item without having a
Product and hence the ID of the Item should indicate to which Product it belongs.

````
Product ID: PRD-1234-5678-9012
Item IDs: ITM-1234-5678-9012-0001, ITM-1234-5678-9012-0002, ITM-1234-5678-9012-0003
````

The primary requirement of such links are that the client object should have reference to the
base object as a property and base object should have a Verbose ID.

Code Example:

```
from connect.utils.peewee.mixins import TransactionalIDMixin, VerboseIDMixin


class Product(VerboseIDMixin):
    SEPARATOR_FREQUENCY = 4
    
    @property
    def prefix(self):
        return 'PRD'

    name = peewee.CharField()

    class Meta:
        database = db


product1 = Product.create(name='Office 365')

print(product1.id)
PRD-6725-9012-6419 

class Item(TransactionalIDMixin):
    SEPARATOR_FREQUENCY = 4
    SUFFIX_LENGTH = 4
    CHAIN_FIELD = 'product'
    
    @property
    def prefix(self):
        return 'ITM'
    
    product = peewee.ForeignKeyField(Product, backref='items')
    name = peewee.CharField()

    class Meta:
        database = db

item = Item.create(product=product, name='example item')
print(item.id)
ITM-6725-9012-6419-0001
```