from feast_global import FEAST_DTYPE

class FeastDataType(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, data_type):
        feast_data_type = list(FEAST_DTYPE.keys())
        if data_type in feast_data_type:
            return data_type
        else:
            raise ValueError(
                f'This is not a defined data type in Feast.'
                f'The following data types are available.{feast_data_type}'
            )

class FeastDataTypeForm(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, data_type):
        feast_data_type_form = list(list(FEAST_DTYPE.values())[0].keys())
        if data_type in feast_data_type_form:
            return data_type
        else:
            raise ValueError(
                f'This is not a defined data type form in Feast.'
                f'The following data type forms are available.{feast_data_type_form}'
            )