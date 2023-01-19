class InfoMessage:

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        """
        training_type — имя класса тренировки
        duration — длительность тренировки в часах
        distance — дистанция в километрах, которую преодолел
        пользователь за время тренировки
        speed — средняя скорость, с которой двигался пользователь
        calories — количество килокалорий, которое израсходовал
        пользовательза время тренировки
        """
        self.training_type = training_type
        self.duration = duration
        self.get_distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.get_distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    """
    M_IN_KM — константа для перевода значений из метров в километры
    LEN_STEP — расстояние, которое спортсмен преодолевает за один шаг/гребок
    MIN_IN_H — перевод часов в минуты
    """
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        """Информационное сообщение о тренировке."""
        """
        action — количество совершённых действий
        duration — длительность тренировки в часах
        weight — вес спортсмена
        """
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """
        Метод для расчета дистанции. Количество действий умножается на длунну
        в метрах и переводится в километры делением на 1000.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """
        Получить среднюю скорость движения.
        Метод для расчета дистанции. Количество действий умножается на длунну
        в метрах и переводится в километры делением на 1000.
        """
        return (self.action * self.LEN_STEP / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            "Определите get_spent_calories в %s." % (self.__class__.__name__)
        )

    def show_training_info(self) -> InfoMessage:
        """
        Метод возвращает объект датакласса InfoMessage путем вызова
        методов расчета.
        """
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    MIN_IN_H: int = 60

    def get_spent_calories(self) -> float:
        """
        Функция расчитывает количество потраченных калорий для бега.
        """
        spent_calories_run = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                                               * self.MIN_IN_H * self.duration
        )

        return spent_calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100
    COEF: int = 2
    """
    action — количество совершённых действий
    duration — длительность тренировки в часах
    weight — вес спортсмена
    height — рост спортсмена
    """
    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** self.COEF
                   / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
            * self.duration * self.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    FRST_COEF: float = 1.1
    SEC_COEF: float = 2
    """
    action — количество совершённых действий
    duration — длительность тренировки в часах
    weight — вес спортсмена
    heightlength_pool — длина бассейна в метрах
    count_pool — сколько раз пользователь переплыл бассейн
    """
    def __init__(
        self,
        action: float,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ):
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.lenght_pool * self.count_pool / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        spent_calories_swm: str = ((self.get_mean_speed() + self.FRST_COEF)
                                   * self.SEC_COEF * self.weight
                                   * self.duration)
        return spent_calories_swm


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    parameters_train: int = {
        "SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    if workout_type in parameters_train:
        return parameters_train[workout_type](*data)


def output(training: Training) -> None:
    """
    Главная функция. Метод show_training_info() есть у базового класса
    тренировки. Он вернет экземпляр класса InfoMessage. А метод get_message()
    вернет строку с подставленными данными тренировки.
    """
    message_train = training.show_training_info()  # экземпляр InfoMessage
    print(message_train.get_message())  # печатаем сообщение встроенным методом


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
