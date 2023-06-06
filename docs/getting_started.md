## Requirements

*peewee-model-utils* runs on python 3.7 or later.

## Install

*peewee-model-utils* is a small python package that can be installed
from the [pypi.org](https://pypi.org/project/peewee-model-utils/) repository.

```
$ pip install peewee-model-utils
```

## Example use of VerboseIDMixin

Following example is showing how to use VerboseIDMixin which helps to generate ID
for a model in a very simple and systematic patter starts with a prefix and followed
by some number of digits.

```
from connect.utils.peewee.mixins import VerboseIDMixin


class Product(VerboseIDMixin):
    SEPARATOR_FREQUENCY = 3
    
    @property
    def prefix(self):
        return 'PRD'

    name = peewee.CharField()

    class Meta:
        database = db


product1 = Product.create(name='Office 365')

print(product1.id)
PRD-672-901-641 
```
