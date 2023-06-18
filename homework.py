# from logging import getLogger  #  логгер

# log = getLogger('homework_oop')
# log.setLevel('INFO')

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Вывод сообщения о тренировке"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000  # метров в километре
    LEN_STEP = 0.65
    MIN_IN_H = 60  # минут в часе

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

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
    CALORIES_WALK_MULTIPLIER_1 = 0.035
    CALORIES_WALK_MULTIPLIER_2 = 0.029
    SPEED_KMH_TO_MS = 0.278  # для перевода км/ч в м/с
    M_IN_SM = 100

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
    CALORIES_SWIM_MULTIPLIER_1 = 1.1
    CALORIES_SWIM_MULTIPLIER_2 = 2
    LEN_STEP = 1.38

    def __init__(self, action: float, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        spent_calories = ((mean_speed + self.CALORIES_SWIM_MULTIPLIER_1)
                          * self.CALORIES_SWIM_MULTIPLIER_2
                          * self.weight * self.duration)
        return spent_calories


WORKOUT_TYPE_MAP = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking
                    }


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in WORKOUT_TYPE_MAP:
        raise KeyError(f'Неверно указан тип тренировки: {workout_type}')
    return WORKOUT_TYPE_MAP[workout_type](*data)


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
