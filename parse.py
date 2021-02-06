import json
from urllib import request, parse



class Parse:

    _url = "https://calcus.ru/currency"
    _currency1 = "RUB"
    _currency2 = "USD"
    _value = 1

    def __init__(self, url=_url, currency1=_currency1, currency2=_currency2, value=_value):
        self._url = url
        self._currency1 = currency1
        self._currency2 = currency2
        self._value = value
        self._response = None
        self._dic = None
        self._result_dic = None
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
    def _make_data(self):



    """Получем данные с запроса"""
    def _get_response(self):
        data = parse.urlencode(self._data)
        data = data.encode('ascii')
        with request.urlopen(self._url, data) as f:
            self._response = f.read()


    @staticmethod
    def fields(currency1, currency2, value, url):
        Parse._url = url
        Parse._currency1 = currency1
        Parse._currency2 = currency2
        Parse._value = value


    def run(self):
        self._get_response()
        self._get_dict()
        print(self._dic)



if __name__ == '__main__':

    pars = Parse(currency1='USD', currency2='RUB', value=20)
    pars.run()

