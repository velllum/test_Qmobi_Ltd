import codecs
import json

from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler

from errors import ServerError
from converter import MoneyConverter


class SimpleHandler(BaseHTTPRequestHandler):
    """
    Класс расширяется базовым классом BaseHTTPRequestHandler
     и реализует работу конвертера валют рубль к доллару и обратно
    """

    def __init__(self, *args, **kwargs):
        """
            - self.pars - объект конвертера MoneyConverter()
            - self.error - объект проверки ввода данных ServerError()
            - self.response_data - словарь хранит данные для вывода
            - self.base_data - словарь хранит все базовые данные
            - self.post_data_dict - словарь хранит данные с POST запроса
            - self.status - объект хранит данные статусов, описаний и кодов ошибок сервера
            - self.item_field - словарь хранит дефолтными данными результата работы конвертера
        :param args:
        :param kwargs:
        """
        self.pars = MoneyConverter()
        self.error = ServerError()

        self.response_data = bytes()
        self.base_data = dict()
        self.post_data_dict = dict()

        self.status = HTTPStatus.OK
        self.item_field = dict(
            Валюта_запроса="Введите конверт. валюту RUB или USD",
            Сумма_запроса="Введите конверт. сумму",
            Валюта_ответа="...",
            Сумма_ответа="..."
        )

        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    @property
    def status_fields(self):
        """
        Создаем поля описывающие состояние статуса сервера.
        Поля содержат по дефолту значение значение статуса сервера 200 OK
        Поля меняют значение, зависящие от свойства self.status
        :return: dict()
        """
        return dict(
            description=self.status.description,
            enum_name=self.status.phrase,
            code=self.status.value,
        )

    @property
    def items_fields(self):
        """
        Передает поля заполненные данными конвертора.
        По умолчанию, поля заполнены дефолтными данными,
        хранящиеся в статическом свойстве _DEFAULT_FIELDS_ITEMS
        :return: self.item_field
        """
        return self.item_field

    @items_fields.setter
    def items_fields(self, dic):
        """
        Получаем обработанное значение от конвертера,
        в виде словаря dict() и сохраняем в self.item_field
        :param dic: > dict()
        :return: None
        """
        self.item_field = dic

    def _defining_status(self):
        """
        Определяем статус запроса, и переопределяем свойство self.status - HTTPStatus
            - Проверяем является ли POST запрос не существующей ссылкой, если да то меняем статус в self.status на HTTPStatus.NOT_IMPLEMENTED
            - Проверяем GET запрос на существование, если условие прошли меняем статус на HTTPStatus.NOT_FOUND
        :return: None
        """
        if self.command == "POST" and self.path != "/":
            self.status = HTTPStatus.NOT_IMPLEMENTED
        elif self.path != "/":
            self.status = HTTPStatus.NOT_FOUND

    def _fill_base_dict(self):
        """
        Проверяет статус self.status на код сервера 200
            - Если статус подтвердился, то заполняем словарь
        наполняем базовый словарь данными
        Переопределяем свойство base_data - основной словарь self.base_data,
        полями из свойства статуса и данными из конвертера
            - Если же нет то тогда предаем только статус об ошибке сервера self.status
        :return: None
        """
        if self.status != 200:
            self.base_data["status"] = self.status_fields
        else:
            self.base_data["status"] = self.status_fields
            self.base_data["items"] = self.items_fields

    def _set_headers(self):
        """
        Заполняем заголовки
            - передаем в запрос, код статуса
            - заполняем заголовки запроса значениями
        :return: None
        """
        self.send_response(self.status.value)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _data_send_response(self):
        """
        Подготавливаем словарь с данными self.base_data, для отправки ответа
            - Преобразует в формат json
            - Кодирует в формат пригодный для вывода кириллических символов
            - Конвертируем в байтовое представление
            - Передаем на хранение в self.response_data
        :return: None
        """
        data = json.dumps(self.base_data, sort_keys=True, indent=4)
        data = codecs.decode(data, 'unicode_escape')
        self.response_data = bytes(data, 'utf8')

    def _get_post_data(self):
        """
        Получает и конвертирует POST данные
            - Получаем данные с post запроса в виде байт строки
            - Декодируем в формат UTF8
            - Конвертируем в JSON и в словарь, сохраняем в self.post_data_dict
        :return: None
        """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = post_data.decode("utf8")
        try:
            self.post_data_dict = dict(json.loads(data))
        except:
            self.post_data_dict = {"Валюта_запроса": "", "Сумма_запроса": 0}

    def _post_check_data_errors(self):
        """
        Проверяем полученные данные POST запроса на правильность ввода.
        Если если словарь вернулся пустым то возвращаем ответ True
        Если нет, то передаем ответ в базовый словарь свойства self.base_data
        :return: bool
        """
        self.error.value = self.post_data_dict
        if self.error.value:
            self.base_data = self.error.value
        return True

    def _get_result_converter(self):
        """
        Обрабатывает данные полученные от конвертера
            - Отправляем данные в конвертер на обработку
            - Возвращенными данными, расширяем словарь что хранится в свойстве self.post_data_dict
            - Переопределяем данные для вывода, что хранятся в свойстве self.items_field
        :return: None
        """
        self.pars.fields = self.post_data_dict  # передаем данные в парсер
        self.post_data_dict.update(self.pars.fields)  #
        self.items_fields = self.post_data_dict  # переопределяем данные в "items"

    def do_GET(self):
        """
        Обрабатываем GET запросы, и выводим в виде json на экран
        :return: None
        """
        self._defining_status()
        self._fill_base_dict()
        self._set_headers()
        self._data_send_response()
        self.wfile.write(self.response_data)

    def do_POST(self):
        """
        Обрабатывает POST запросы, и передает для вывода, json на экран
        :return: None
        """
        self._defining_status()
        self._get_post_data()

        if self._post_check_data_errors():
            self._get_result_converter()
            if not self.base_data:
                self._fill_base_dict()

        self._set_headers()
        self._data_send_response()
        self.wfile.write(self.response_data)


class Server:
    """
    Запуск сервера переменная _SERVER_ADDRESS данные по умолчанию любой числовой адрес и порт по умолчанию 8000(0.0.0.0:8000)
        - вводим адрес
        - вводим порт
    """
    _SERVER_CLASS = SimpleHandler
    _SERVER_ADDRESS = ('', 8000)

    def __init__(self):
        handler = HTTPServer(Server._SERVER_ADDRESS, Server._SERVER_CLASS)
        try:
            print(
                f"(START) Serving HTTP on {handler.server_address[0]} port {handler.server_port} (http://{handler.server_address[0]}:{handler.server_port}/)")
            handler.serve_forever()
        except KeyboardInterrupt:
            print(
                f"(STOP) Serving HTTP on {handler.server_address[0]} port {handler.server_port} (http://{handler.server_address[0]}:{handler.server_port}/)")
            handler.server_close()


if __name__ == '__main__':
    server = Server()
