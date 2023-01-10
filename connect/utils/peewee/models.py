import peewee


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
