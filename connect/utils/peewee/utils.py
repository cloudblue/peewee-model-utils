import random
from textwrap import wrap


def _wrap_id(suffix_length, separator_frequency, separator, id_sequence):
    if separator_frequency is None:
        separator_frequency = 4 if suffix_length % 4 == 0 else 3
    return f"{separator}".join(wrap(id_sequence, separator_frequency))


def _template_verbose_id(prefix, separator, verbose_id):
    return '{name}{separator}{id}'.format(
        name=prefix, separator=separator, id=verbose_id)


def _generate_verbose_id(
    prefix,
    suffix_length,
    separator_frequency,
    separator,
    id_sequence,
):
    _wrapped_id = _wrap_id(
        suffix_length, separator_frequency, separator, id_sequence)

    return _template_verbose_id(prefix, separator, _wrapped_id)


def generate_verbose_id(
    prefix,
    suffix_length,
    separator_frequency,
    separator,
):
    """
    Generate verbose id

    :param prefix: str: verbose id prefix
    :param suffix_length: int: verbose id suffix length
    :param separator_frequency: int: number of separators during generating id
    :param separator: str: verbose id separator

    :return: verbose id
    :rtype: str
    """
    return _generate_verbose_id(
        prefix,
        suffix_length,
        separator_frequency,
        separator,
        random_numeric_string_sequence(suffix_length),
    )


def random_numeric_string_sequence(length):
    """
    Generate random numeric string with passed length

    :param length: int: output string length
    :return: random numeric string
    :rtype: str
    """
    if length <= 0:
        return ''

    return str(random.randint(
        1 * 10**(length - 1),
        1 * 10**length - 1),
    )


def is_verbose_id(prefix, separator, id_value):
    """
    Check if passed value is verbose id value with particular prefix

    :param prefix: str: verbose id prefix
    :param separator: str: verbose id separator
    :param id_value: str: checked value
    :return: if passed id_value is valid verbose id
    :rtype: bool
    """
    return id_value.startswith(f'{prefix}{separator}')
