import peewee

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


class OrderedModelMixin(peewee.Model):
    """
    The mixin adds integer property 'position' which allows to sort objects within queryset
    automatically. It also adds 'sort' method to put object after/before specified one in the
    sequence.
    """

    ORDER_POSITION_STEP = 10000
    START_POSITION = 0
    is_position_up = True

    position = peewee.BigIntegerField(null=True, index=True)

    class Meta:
        abstract = True

    @property
    def last_element(self):
        return self.__class__.select().order_by(self.__class__.position.desc()).first()

    @property
    def first_element(self):
        return self.__class__.select().order_by(self.__class__.position.asc()).first()

    def save(self, *args, **kwargs):
        if not self.position:
            self.position = getattr(self.last_element, 'position', 0) + self.ORDER_POSITION_STEP

        super().save(*args, **kwargs)

    def __update_position_query(self, is_position_up):
        mark = 1 if is_position_up else -1
        return self.__class__.update(
            position=self.__class__.position + mark * self.ORDER_POSITION_STEP)

    def __filter_by_gt_lt(self, query, gt_data, lte_data):
        filtered_resource = query.where(
            self.__class__.position > gt_data,
            self.__class__.position < lte_data,
        )

        return filtered_resource

    def __sort_after(self, after):
        if not after:
            filtered_resources_update = self.__update_position_query(self.is_position_up).where(
                self.__class__.position < self.position,
            )
            self.position = self.first_element.position

        elif self.position and after.position >= self.position:
            filtered_resources_update = self.__update_position_query(False).where(
                self.__class__.position > self.position,
                self.__class__.position <= after.position,
            )
            self.position, self.is_position_up = after.position, False

        else:
            filtered_resources_update = self.__filter_by_gt_lt(
                self.__update_position_query(self.is_position_up),
                after.position,
                self.position,
            )
            # When we undo last resource deleting, it should be placed with the
            # highest position but other resources positions should not be touched

            filtered_resources_select = self.__filter_by_gt_lt(
                self.__class__.select(),
                after.position,
                self.position,
            )
            if filtered_resources_select.exists():
                # Handle the case when the user move resource from bottom to higher place
                self.position = filtered_resources_select.first().position

        return filtered_resources_update

    def __sort_before(self, before):
        if self.position and before.position > self.position:
            self.is_position_up = False
            filtered_resource = self.__filter_by_gt_lt(
                self.__update_position_query(self.is_position_up),
                self.position,
                before.position,
            )
            self.position = int(before.position) - self.ORDER_POSITION_STEP

        elif self.position > before.position:
            filtered_resource = self.__update_position_query(self.is_position_up).where(
                self.__class__.position >= before.position,
                self.__class__.position < self.position,
            )
            self.position = before.position

        else:
            raise ValueError("Element 'before' is invalid.")

        return filtered_resource

    def sort(self, after=None, before=None):
        """
            :param before: target instance for before
            :param after: target instance for after
            :return: Nothing
        """
        if before and self._pk == before._pk or after and self._pk == after._pk:
            raise ValueError("Elements must be different.")
        elif before:
            filtered_resource = self.__sort_before(before)
        else:
            filtered_resource = self.__sort_after(after)

        filtered_resource.execute()
        self.save()
