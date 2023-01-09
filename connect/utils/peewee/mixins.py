from connect.utils.peewee.models import VerboseBase
from connect.utils.peewee.utils import generate_verbose_id


class VerboseIDMixin(VerboseBase):
    """
        Mixin for common verbose IDs generation. Generated ID format depends on implementing class
        properties:
            * prefix - alphanumeric prefix, for example 'PRD' or 'AGU', required
            * SEPARATOR - symbol (or substring) to separate ID parts, default '-'
            * SUFFIX_LENGTH - number of digits, default 9
            * SEPARATOR_FREQUENCY - digits in one chunk, default 3 or 4, depending on SUFFIX_LENGTH

        For example:
            prefix='PRD', SUFFIX_LENGTH=5, SEPARATOR_FREQUENCY=5: 'PRD-12345'
            prefix='PRD', SUFFIX_LENGTH=10, SEPARATOR_FREQUENCY=5: 'PRD-12345-12345'
            prefix='AGP', SUFFIX_LENGTH=12, SEPARATOR_FREQUENCY=5: 'AGP-12345-12345-12'
            prefix='TCR', SUFFIX_LENGTH=7, SEPARATOR_FREQUENCY=None: 'TCR-123-123-1'

        IMPORTANT: This mixin can not be used for bulk_create operations.
        """
    SUFFIX_LENGTH = 9
    SEPARATOR_FREQUENCY = None

    def _generate_id(self, using=None, iteration=0):
        return generate_verbose_id(
            self.prefix,
            self.SUFFIX_LENGTH,
            self.SEPARATOR_FREQUENCY,
            self.SEPARATOR,
        )
