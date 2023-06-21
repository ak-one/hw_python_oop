from dataclasses import asdict, dataclass
from typing import Type, ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вывод сообщения о тренировке"""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000  # метров в километре
    LEN_STEP: float = 0.65  # длина шага
    MIN_IN_H: int = 60  # минут в часе

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18  # множитель средней скорости
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79  # множитель смещения скорости

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed = self.get_mean_speed()
        duration_m = self.duration * self.MIN_IN_H
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.weight / self.M_IN_KM * duration_m)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WALK_MULTIPLIER_1: float = 0.035  # множитель для расчета калорий
    CALORIES_WALK_MULTIPLIER_2: float = 0.029  # множитель для расчета калорий
    SPEED_KMH_TO_MS: float = 0.278  # для перевода км/ч в м/с
    M_IN_SM: int = 100  # сантиметров в метре

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        height_m = self.height / self.M_IN_SM
        mean_speed_m_s = self.get_mean_speed() * self.SPEED_KMH_TO_MS
        duration_min = self.duration * self.MIN_IN_H
        spent_calories = ((self.CALORIES_WALK_MULTIPLIER_1 * self.weight
                           + (mean_speed_m_s**2 / height_m)
                           * self.CALORIES_WALK_MULTIPLIER_2
                           * self.weight) * duration_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_SWIM_MULTIPLIER_1: float = 1.1  # множитель для расчета калорий
    CALORIES_SWIM_MULTIPLIER_2: int = 2  # множитель для расчета калорий
    LEN_STEP = 1.38

    def __init__(self, action: float, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed()
                           + self.CALORIES_SWIM_MULTIPLIER_1)
                          * self.CALORIES_SWIM_MULTIPLIER_2
                          * self.weight * self.duration)
        return spent_calories


WORKOUT_TYPE_MAP: dict[str, Type[Training]] = {'SWM': Swimming,
                                               'RUN': Running,
                                               'WLK': SportsWalking}


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout := WORKOUT_TYPE_MAP.get(workout_type):
        return workout(*data)
    raise ValueError(f'Неверно указан тип тренировки: {workout_type}')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
