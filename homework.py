from dataclasses import dataclass
from typing import Dict, Union, Callable, List


@dataclass(repr=False, eq=False)
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Формирует и возращает информационную переменную строкового типа."""
        message: str = (f'Тип тренировки: {self.training_type};'
                        f' Длительность: {self.duration:.3f} ч.;'
                        f' Дистанция: {self.distance:.3f} км;'
                        f' Ср. скорость: {self.speed:.3f} км/ч;'
                        f' Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOUR_TO_MINUTE = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Определите метод get_spent_calories'
            f' в {self.__class__.__name__}.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message_obj: InfoMessage = InfoMessage(self.__class__.__name__,
                                                    self.duration,
                                                    self.get_distance(),
                                                    self.get_mean_speed(),
                                                    self.get_spent_calories())
        return info_message_obj


@dataclass(repr=False, eq=False)
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    SWIM_CALORIE_COEFF_1 = 1.1
    SWIM_CALORIE_COEFF_2 = 2

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения для плавания."""
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Подсчет калорий для плавания."""
        calories: float = ((self.get_mean_speed() + self.SWIM_CALORIE_COEFF_1)
                           * self.SWIM_CALORIE_COEFF_2 * self.weight)
        return calories


class Running(Training):
    """Тренировка: бег."""

    RUN_CALORIE_COEFF_1 = 18
    RUN_CALORIE_COEFF_2 = 20

    def get_spent_calories(self) -> float:
        """Подсчет калорий для бега."""
        calories: float = ((self.RUN_CALORIE_COEFF_1
                            * self.get_mean_speed()
                            - self.RUN_CALORIE_COEFF_2)
                           * self.weight / self.M_IN_KM
                           * self.duration * self.HOUR_TO_MINUTE)
        return calories


@dataclass(repr=False, eq=False)
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WALK_CALORIE_COEFF_1 = 0.035
    WALK_CALORIE_COEFF_2 = 0.029

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        """Подсчет калорий для спортивной ходьбы."""
        calories: float = ((self.WALK_CALORIE_COEFF_1 * self.weight
                            + (self.get_mean_speed() ** 2 // self.height)
                            * self.WALK_CALORIE_COEFF_2 * self.weight)
                           * self.duration * self.HOUR_TO_MINUTE)
        return calories


def read_package(workout_type: str,
                 data: List[Union[int, float]]
                 ) -> Union[Training, None]:
    """Прочитать данные полученные от датчиков."""
    dictionary_type = (Dict[str, (Callable[[Training], None])])
    choose: dictionary_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    current_training: Training = choose.get(workout_type)(*data)
    return current_training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
            main(training)
        except ValueError:
            print(f'Запрошенный тип тренировки {workout_type} не найден!')
