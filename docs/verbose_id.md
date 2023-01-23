## Introduction to Verbose ID

In modern applications, different entities representing the real world
objects are not only present within the application but also used to identify
those objects outside the application. These occurrences can be in terms of
integrations which connects with each other and co-operate to achieve a big goal.

In such cases, it is essential to have a common way to identify the objects
properties with the ID that represent the object.

Now look at the following example:

```PRD-928-562-751```

Here ```PRD``` represents the object type, and we can understand that the object is
of type ```Product``` which has a prefix of ```PRD```.

This approach will make the communication among the parties much easy to understand 
during operational environment like during raising a problem or communication for 
progress in any operational flow.

## Example use of VerboseIDMixin

Following example is showing how to use VerboseIDMixin which helps to generate ID
for a model in a very simple and systematic patter starts with a prefix and followed
by some number of digits.

``` python
from connect.utils.peewee.mixins import VerboseIDMixin


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
```