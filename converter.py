import json
from urllib import request, parse


class MoneyConverter:
    """
    Класс конвертирует валюту по указанному значению  в словаре
    пример запроса:
        {
            "Валюта_запроса": "USD",
            "Сумма_запроса": 3
        }

    пример ответа:
        {
            "Валюта_ответа": "RUB",
            "Сумма_ответа": "222,78"
        }

    Отправка запроса через переопределение свойства объекта obj.fields:
        obj.fields = dict()

    Возврат:
       result = obj.fields
       print(result)

  ===================================================================================

    Статические свойства по дефолту
    """
    _URL = "https://calcus.ru/currency"
    _CURRENCY1 = "RUB"
    _CURRENCY2 = "USD"
    _VALUE = 1

    def __init__(self, currency1=_CURRENCY1, value=_VALUE):
        """
            - self.url - хранит адрес сайта "https://calcus.ru/currency"
            - self.currency1 - Валюта_запроса запроса RUB или USD
            - self.value - Сумма_запроса тип число
            - self.currency2 - Валюта_ответа RUB или USD
            - self.response - ответ от сервера
            - self.base_dic - базовый словарь
            - self.form_data - словарь хранит данные для отправки в запроса

        :param currency1:
        :param value:
        """
        self.url = MoneyConverter._URL
        self.currency1 = currency1
        self.value = value
        self.currency2 = None
        self.response = None
        self.base_dic = None
        self.result_dic = None
        self.form_data = None

    @property
    def fields(self):
        """
        Отправляет словарь с ответом
        :return: None
        """
        return self.result_dic

    @fields.setter
    def fields(self, dic):
        """
        Принимает данные для обработки
        Сохранят валюту запроса в self.currency1
        Сохранят сумму запроса в self.value
        :param dic:
        :return: None
        """
        self.currency1 = dic.get('Валюта_запроса')
        self.value = dic.get('Сумма_запроса')
        self.run()

    def _get_currency2(self):
        """
        Определяет валюту для ответа, сохраняет в self.currency2
        :return: None
        """
        if self.currency1 != MoneyConverter._CURRENCY1:
            self.currency2 = MoneyConverter._CURRENCY1
        else:
            self.currency2 = MoneyConverter._CURRENCY2

    def _get_data(self):
        """
        Собираем данные, что будут подставляться в запрос
        свойство self.form_data
        :return: None
        """
        self.form_data = {
            'calculate': 1,
            'value': self.value,
            'currency1': self.currency1,
            'currency2': self.currency2,
        }

    def _get_dict(self):
        """
        Преобразует данные ответа в словарь
        Декодирует в UTF8, конвертирует в JSON -> dict()
        Сохраняет в self.base_dic
        :return: None
        """
        if self.response:
            text = self.response.decode("utf8")
            self.base_dic = dict(json.loads(text))

    def _make_result(self):
        """
        Собирает данные результата ответа конвертера
        Сохраняет в self.result_dic
        :return: None
        """
        self.result_dic = dict(
            Валюта_ответа=self.base_dic.get("currency2"),
            Сумма_ответа=self.base_dic.get("value"),
        )

    def _get_response(self):
        """
        Делает запрос в конвертер, ответ сохраняет в self.response
        :return: None
        """
        data = parse.urlencode(self.form_data)
        data = data.encode('ascii')
        with request.urlopen(self.url, data) as f:
            self.response = f.read()

    def run(self):
        """
        Функция запуска скрипта
        :return: None
        """
        self._get_currency2()
        self._get_data()
        self._get_response()
        self._get_dict()
        self._make_result()
