from typing import Any, ClassVar, Dict, Type

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

from .validations import BANK_NAMES, BANKS, compute_control_digit


class Clabe(str):
    """
    Based on: https://es.wikipedia.org/wiki/CLABE
    """

    strip_whitespace: ClassVar[bool] = True
    min_length: ClassVar[int] = 18
    max_length: ClassVar[int] = 18

    def __init__(self, clabe: str) -> None:
        self.bank_code_abm = clabe[:3]
        self.bank_code_banxico = BANKS[clabe[:3]]
        self.bank_name = BANK_NAMES[self.bank_code_banxico]

    @property
    def bank_code(self) -> str:
        return self.bank_code_banxico

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> Dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update(
            type="string",
            pattern="^[0-9]{18}$",
            description="CLABE (Clave Bancaria Estandarizada)",
            examples=["723010123456789019"],
        )
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _: Type[Any],
        __: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(
                min_length=cls.min_length,
                max_length=cls.max_length,
                strip_whitespace=cls.strip_whitespace,
            ),
        )

    @classmethod
    def _validate(cls, clabe: str) -> 'Clabe':
        if not clabe.isdigit():
            raise PydanticCustomError('clabe', 'debe ser numérico')
        if clabe[:3] not in BANKS:
            raise PydanticCustomError(
                'clabe.bank_code', 'código de banco no es válido'
            )
        if clabe[-1] != compute_control_digit(clabe):
            raise PydanticCustomError(
                'clabe.control_digit', 'clabe dígito de control no es válido'
            )
        return cls(clabe)
