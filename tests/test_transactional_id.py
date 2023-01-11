import peewee
import pytest

from connect.utils.peewee.exceptions import (
    InvalidVerboseIdException,
    MissedChainFieldException,
    NullFieldValueException,
)
from connect.utils.peewee.mixins import TransactionalIDMixin, VerboseIDMixin
from tests.utils import db, use_test_database


class VerboseIDModel(VerboseIDMixin):

    name = peewee.CharField(null=True)

    @property
    def prefix(self):
        return 'TEST-VERBOSE-ID'

    class Meta:
        database = db


class TransactionalIDModel(TransactionalIDMixin):
    SUFFIX_LENGTH = 3
    CHAIN_FIELD = 'vid'

    vid = peewee.ForeignKeyField(VerboseIDModel, backref='transactionalIDs')

    @property
    def prefix(self):
        return 'TEST-TRAN-ID'

    class Meta:
        database = db


class TransactionalIDNoSafeModel(TransactionalIDMixin):
    SUFFIX_LENGTH = 3
    CHAIN_FIELD = 'vid'
    SAFE_GENERATE = False

    vid = peewee.ForeignKeyField(VerboseIDModel, backref='transactionalIDs')

    @property
    def prefix(self):
        return 'TEST-TRAN-ID'

    class Meta:
        database = db


class WrongTransactionalIDModel(TransactionalIDMixin):
    SUFFIX_LENGTH = 3

    vid = peewee.ForeignKeyField(VerboseIDModel, backref='transactionalIDs')

    @property
    def prefix(self):
        return 'TEST-TRAN-ID'

    class Meta:
        database = db


@use_test_database(models=(VerboseIDModel, TransactionalIDModel))
def test_transactional_id_generation():
    v_id_obj = VerboseIDModel.create()

    prefix = v_id_obj.id.replace('TEST-VERBOSE-ID', 'TEST-TRAN-ID')

    for _ in range(1, 4):
        tran_id_obj = TransactionalIDModel.create(vid=v_id_obj)
        assert tran_id_obj.id == f'{prefix}-00{_}'


@use_test_database(models=(VerboseIDModel, TransactionalIDNoSafeModel))
def test_transactional_id_generation_no_safe():
    v_id_obj = VerboseIDModel.create(id='NOT-VALID-ID-0001')

    for _ in range(1, 4):
        tran_id_obj = TransactionalIDNoSafeModel.create(vid=v_id_obj)
        assert tran_id_obj.id.startswith('TEST-TRAN-ID')
        assert tran_id_obj.id.endswith('001')


@use_test_database(models=(VerboseIDModel, TransactionalIDModel))
def test_invalid_chain_field_id():
    v_id_obj = VerboseIDModel.create(id='ID-0001')

    with pytest.raises(InvalidVerboseIdException):
        TransactionalIDModel.create(vid=v_id_obj)


@use_test_database(models=(VerboseIDModel, WrongTransactionalIDModel))
def test_invalid_chain_field_property():
    v_id_obj = VerboseIDModel.create()

    with pytest.raises(MissedChainFieldException):
        WrongTransactionalIDModel.create(vid=v_id_obj)


@use_test_database(models=(VerboseIDModel, TransactionalIDModel))
def test_none_chain_field_property_value():
    with pytest.raises(NullFieldValueException):
        TransactionalIDModel.create(vid='None')
