from unittest.mock import patch

import peewee
import pytest

from connect.utils.peewee.mixins import VerboseIDMixin
from tests.utils import db, use_test_database


class VerboseIDModel(VerboseIDMixin):
    @property
    def prefix(self):
        return 'TEST-VERBOSE-ID'

    name = peewee.CharField()

    class Meta:
        database = db


class VerboseIDModelWithSeparatorFrequency(VerboseIDMixin):
    SEPARATOR_FREQUENCY = 3

    @property
    def prefix(self):
        return 'TEST-VERBOSE-ID-SEP'

    name = peewee.CharField(null=False)

    class Meta:
        database = db


@use_test_database(models=(VerboseIDModel,))
def test_verbose_id_generation():
    VerboseIDModel.create(name='Test name')

    for obj in (VerboseIDModel.select()):
        assert obj.id
        assert obj.id.startswith('TEST-VERBOSE-ID')


@use_test_database(models=(VerboseIDModel,))
@patch('connect.utils.peewee.mixins.generate_verbose_id', return_value='TEST-VERBOSE-ID-0001')
def test_verbose_id_error_on_duplicate(mock_generate_verbose_id):
    VerboseIDModel.create(name='Test name 1')
    with pytest.raises(Exception):
        VerboseIDModel.create(name='Test name 2')


@use_test_database(models=(VerboseIDModelWithSeparatorFrequency,))
def test_verbose_id_generation_with_seperator_frequency():
    VerboseIDModelWithSeparatorFrequency.create(name='Test name')

    for obj in (VerboseIDModelWithSeparatorFrequency.select()):
        assert obj.id
        assert obj.id.startswith('TEST-VERBOSE-ID-SEP')


@use_test_database(models=(VerboseIDModel,))
def test_integrity_error():
    with pytest.raises(peewee.IntegrityError):
        VerboseIDModel.create()


@use_test_database(models=(VerboseIDModel,))
def test_id_already_present():
    VerboseIDModel.create(id='TEST-ID', name='test name')

    obj = VerboseIDModel.get(id='TEST-ID')

    assert obj
