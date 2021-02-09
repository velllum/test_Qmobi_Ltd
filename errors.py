


class ServerError(Exception):

    def __init__(self):
        """
        Проверка данных перед отправкой
        """
        self.dic = dict()
        self.error_message = dict(
            error_message=dict()
        )


    @property
    def value(self):
        """
        передаем словарь с сообщением в словарь статус
        :return: self.error_message
        """
        if self.error_message["error_message"]:
            return self.error_message


    @value.setter
    def value(self, dic):
        """
        Получить словарь пост запроса
        :param dic:
        :return: None
        """
        self.dic = dic
        self.run()



    def _str_check_error(self, value):
        """
        Проверка строкового значения на ошибки
        :param value:
        :return: None
        """
        try:
            value_ = value.upper()
            if value_ != 'RUB' and value_ != 'USD':
                self.error_message["error_message"]["Валюта_запроса"] = "Укажите поле валюты 'RUB' или 'USD'"
        except Exception as e:
            print(f"ERROR {value} - ", e)


    def _num_check_error(self, value):
        """
        Проверка числового значения на ошибки
        :param value:
        :return: None
        """
        try:
            if type(value) != int and type(value) != float:
                self.error_message["error_message"]["Сумма_запроса"] = "Значение поля сумма должно быть чиловым"
            elif value <= 0:
                self.error_message["error_message"]["Сумма_запроса"] = "Указанное число меньше ноля, или ноль"
        except Exception as e:
            print(f"ERROR {value} - ", e)



    def  run(self):
        """
        Функция старта
        :return: None
        """
        self._str_check_error(self.dic["Валюта_запроса"])
        self._num_check_error(self.dic["Сумма_запроса"])

