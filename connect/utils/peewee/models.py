import functools

import peewee
from peewee import DoesNotExist

from connect.utils.peewee.exceptions import (
    InvalidVerboseIdException,
    MissedChainFieldException,
    NullFieldValueException,
)
from connect.utils.peewee.utils import is_verbose_id


class VerboseBase(peewee.Model):
    SEPARATOR = '-'
    SUFFIX_LENGTH = 9

    MAX_ID_GENERATION_ITERATIONS = 10
    MAX_SAVE_ITERATIONS = 5
    ITERATION_ERROR = "Couldn't generate ID."
    PRIMARY_KEY_ERROR = "At least one field should be primary key."

    # TODO: need to think about case, when you need another field as primary field
    # fix in code is applied, but need to decide how to override this field definition
    id = peewee.CharField(primary_key=True)

    class Meta:
        abstract = True

    @property
    def prefix(self):  # pragma: no cover
        raise NotImplementedError

    def _generate_id(self, iteration=0):  # pragma: no cover
        raise NotImplementedError

    def generate_id_with_check(self):
        pk = self._generate_id()

        i = 1
        while self.__class__.select().where(self.__class__.id == pk).exists():
            pk = self._generate_id(iteration=i)
            i += 1

            if i > self.MAX_ID_GENERATION_ITERATIONS:
                raise Exception(self.ITERATION_ERROR)
        return pk

    def generate_id(self):
        self.id = self.generate_id_with_check()

    def save(self, *args, **kwargs):
        if not self.id:
            kwargs.pop('force_insert', None)
            self.generate_id()
            try:
                return super().save(*args, force_insert=True)
            except peewee.IntegrityError as e:
                if '(id)=' not in str(e.orig):
                    raise e
                else:
                    raise Exception(
                        f'Cannot generate ID after {self.MAX_PK_ITERATIONS} iterations.')
        return super().save(*args, **kwargs)


class TransactionalIDBase(VerboseBase):
    SUFFIX_LENGTH = 3
    CHAIN_FIELD = None
    SAFE_GENERATE = True

    class Meta:
        abstract = True

    def _get_base_id(self, chain_field):
        chain_prefix_length = len(chain_field.prefix + self.SEPARATOR)
        if is_verbose_id(chain_field.prefix, chain_field.SEPARATOR, chain_field.id):
            return chain_field.id[chain_prefix_length:]
        elif self.SAFE_GENERATE:
            raise InvalidVerboseIdException(chain_field.id)
        else:
            return chain_field.generate_id_with_check()[chain_prefix_length:]

    def _rgetattr(self, attr):

        def _getattr(obj, attr):
            try:
                return getattr(obj, attr)
            except DoesNotExist:
                return None

        return functools.reduce(_getattr, attr, self)

    def _validate_chain_field(self):
        if self.CHAIN_FIELD is None:
            raise MissedChainFieldException(self.__class__)

        chain_field_value = self._rgetattr(self.CHAIN_FIELD.split('__'))

        if chain_field_value is None:
            raise NullFieldValueException(self.CHAIN_FIELD)

        return chain_field_value
