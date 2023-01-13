class CommonModelMixinException(Exception):
    """
    Base Common Model Mixins exception
    """
    pass


class MissedFieldException(CommonModelMixinException):
    """
    Model exception when mixin cannot find required fields
    """

    field_name = None  # field name

    def __init__(self, class_instance):
        """
        :param type class_instance: class type
        """
        super().__init__(f'You have to set {self.field_name} for {class_instance}')


class NullFieldValueException(CommonModelMixinException):
    """
    Common null field value exception
    """
    def __init__(self, field_name):
        """
        :param str field_name: name of null field
        """
        self.field_name = field_name

        super().__init__(f'You can not provide null value in {field_name}')


class MissedChainFieldException(MissedFieldException):
    """
    Missed CHAIN_FIELD property in class definition
    """
    field_name = 'CHAIN_FIELD'


class MissedPositionFieldException(MissedFieldException):
    """
    Missed POSITION_FIELD property in class definition
    """
    field_name = 'POSITION_FIELD'


class InvalidVerboseIdException(CommonModelMixinException):
    """
    Not a verbose id passed for base calculation
    """
    def __init__(self, id_value):
        super().__init__(f'Invalid Verbose ID passed: {id_value}')
