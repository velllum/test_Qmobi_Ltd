import json
from urllib import request, parse



class Parse:

    _URL = "https://calcus.ru/currency"
    _CURRENCY1 = "RUB"
    _CURRENCY2 = "USD"
    _VALUE= 1


    def __init__(self, currency1=_CURRENCY1, value=_VALUE):
        self._url = "https://calcus.ru/currency"
        self._currency1 = currency1
        self._value = value
        self._currency2 = None
        self._response = None
        self._dic = None
        self._result_dic = None


    """Определить значение коверитируемой валюты"""
    def _get_currency2(self):
        if self._currency1 != Parse._CURRENCY1:
            self._currency2 = Parse._CURRENCY1
        else:
            self._currency2 = Parse._CURRENCY2


    """собираем данные запроса"""
    def _get_data(self):
        self._data = {
            'calculate': 1,
            'value': self._value,
            'currency1': self._currency1,
            'currency2': self._currency2,
        }


    """Преобразуем данные в словарь"""
    def _get_dict(self):
        text = self._response.decode("utf8")
        self._dic = dict(json.loads(text))


    """Собираем данные"""
    def _make_result(self):
        self._result_dic = dict(
            Валюта_ответа=self._dic.get("currency2"),
            Сумма_ответа=self._dic.get("value"),
        )


    """Получем данные с запроса"""
    def _get_response(self):
        data = parse.urlencode(self._data)
        data = data.encode('ascii')
        with request.urlopen(self._url, data) as f:
            self._response = f.read()


    """Функция выполнения программы"""
    def run(self):
        self._get_currency2()
        self._get_data()
        self._get_response()
        self._get_dict()
        self._make_result()


    """Получить словарь с результатом"""
    @property
    def fields(self):
        return self._result_dic


    """Заполняем поля"""
    @fields.setter
    def fields(self, dic):
        self._currency1 = dic.get('Валюта_запроса')
        self._value = dic.get('Сумма_запроса')
        self.run()


# if __name__ == '__main__':
#
#     pars = Parse()
#     dic = dict(currency1='RUB', value=20)
#     pars.fields = dic
#
#     print(pars.fields)

