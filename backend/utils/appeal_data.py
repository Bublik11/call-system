import re
from dataclasses import dataclass, asdict


class ValidatePhoneError(Exception):
    """Ошибка валидации номера телефона"""

    pass


@dataclass
class Appeal:
    """Дата-класс для обработки и валидации данный из обращений"""

    surname: str
    name: str
    patronymic: str
    phone_number: str | int
    message: str

    # Валидатор для пост обработки данных, в случае если данные не коректны вызывается ошибка
    def __post_init__(self):
        if not re.fullmatch(r"^\+7[\d]{10}$", self.phone_number):
            raise ValidatePhoneError('The phone number entered is incorrect.')

    def __str__(self) -> str:
        return str(asdict(self))

    def asdict(self) -> dict:
        return asdict(self)
