class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:

        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}. ')
    pass


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # константа 1 шаг = 0.65м
    M_IN_KM: int = 1000  # константа для перевода м в км
    TIME_MINUTES: int = 60  # константа минуты в часах

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        pass
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message
        pass


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18  # константа, коэффициент подсчета калорий
    coeff_calorie_2: int = 20  # константа, коэффициент подсчета калорий

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_callories_run = ((self.coeff_calorie_1 * self.get_mean_speed()
                               - self.coeff_calorie_2) * self.weight
                               / self.M_IN_KM * self.duration
                               * self.TIME_MINUTES)
        return spent_callories_run
        pass
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_3: float = 0.035  # константа, коэффициент подсчета калорий
    coeff_calorie_4: float = 0.029  # константа, коэффициент подсчета калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_callories_walk = ((self.coeff_calorie_3 * self.weight
                                + (self.get_mean_speed()**2 // self.height)
                                * self.coeff_calorie_4 * self.weight)
                                * self.duration * self.TIME_MINUTES)
        return spent_callories_walk
    pass


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # константа 1 гребок = 1.38м
    coeff_calorie_5: float = 1.1  # константа, коэффициент подсчета калорий
    coeff_calorie_6: int = 2  # константа, коэффициент подсчета калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_callories_swim = ((self.get_mean_speed() + self.coeff_calorie_5)
                                * self.coeff_calorie_6 * self.weight)
        return spent_callories_swim

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    training = workouts[workout_type](*data)
    return training
    pass


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
