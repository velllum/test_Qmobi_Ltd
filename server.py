import codecs
import json

from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler

from errors import ServerError
from parse import Parse


class SimpleHandler(BaseHTTPRequestHandler):

    _DEFAULT_FIELDS_ITEMS = dict(
        Валюта_запроса="Введите конверт. валюту RUB или USD",
        Валюта_ответа="...",
        Сумма_запроса="Введите конверт. сумму",
        Сумма_ответа="..."
    )

    def __init__(self, *args, **kwargs):
        self.pars = Parse()
        self.error = ServerError()

        self.post_request_data = bytes()
        self.response_data = bytes()
        self.base_data = dict()
        self.post_data_dict = dict()

        self.status = HTTPStatus.OK
        self.item_field = SimpleHandler._DEFAULT_FIELDS_ITEMS
        self.state_field = dict()

        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)



    def _get_fields(self):
        """
        заполняет поля статуса
        :return: None
        """
        self.state_field = dict(
            description=self.status.description,
            enum_name=self.status.phrase,
            code=self.status.value,
        )

    @property
    def status_fields(self):
        """
        геттер передает поля статуса
        :return: dict()
        """
        self._get_fields()  # поля по умолчанию
        return self.state_field


    @status_fields.setter
    def status_fields(self, state_field):
        """
        Получить поля с данными статуса
        :param state_field: > dict()
        :return: None
        """
        self.state_field = state_field


    @property
    def items_fields(self):
        """
        Получить поля с данными конвертера
        :return: None
        """
        return self.item_field


    @items_fields.setter
    def items_fields(self, dic):
        """
        Собрать поля с данными конвертера
        :param dic: > dict()
        :return: None
        """
        self.item_field = dic


    def _defining_status(self):
        """
        Определяем статус запроса
        Переопределяем свойство status - HTTPStatus
        :return: None
        """
        if self.command == "POST" and self.path != "/":
            self.status = HTTPStatus.NOT_IMPLEMENTED
        elif self.path != "/":
            self.status = HTTPStatus.NOT_FOUND


    def _fill_base_dict(self):
        """
        наполняем базовый словарь данными
        Переопределяем свойство base_data - основной словарь
        :return: None
        """
        if self.status != 200:
            self.base_data["status"] = self.status_fields
        else:
            self.base_data["status"] = self.status_fields
            self.base_data["items"] = self.items_fields


    def _set_headers(self):
        """
        Заполняем заголовки запроса
        :return: None
        """
        self.send_response(self.status.value)
        self.send_header('Content-type', 'application/json')
        self.end_headers()


    def _data_send_response(self):
        """
        Подготавливаем словарь с данными, для отправки ответа
        :return: None
        """
        data = json.dumps(self.base_data, sort_keys=True, indent=4)
        data = codecs.decode(data, 'unicode_escape')
        self.response_data = bytes(data, 'utf8')


    def _get_post_data(self):
        """
        Получаем данные с post запроса
        :return: None
        """
        content_length = int(self.headers['Content-Length'])
        self.post_request_data = self.rfile.read(content_length)


    def _get_dict(self):
        """
        Конвертируем полученные post данные в словарь self.post_data_dict
        :return: None
        """
        data = self.post_request_data.decode("utf8")
        self.post_data_dict = dict(json.loads(data))

    # """Проверка отправленных данных на сервер"""
    # def _post_data_validation(self):
    #     text = self.post_data_dict["Валюта_запроса"]
    #     if not isinstance(text, str):
    #         raise ValueError("Вы ввели число введите пожалуйста текст")
    #         # self.status_fields = "Вы ввели число введите пожалуйста текст"


    def _get_result_converter(self):
        """
        Получить результат работы конвертора
        :return: None
        """
        self.pars.fields = self.post_data_dict  # передаем данные в парсер
        self.post_data_dict.update(self.pars.fields)  # расширяем данными из парсера
        self.items_fields = self.post_data_dict  # переопределяем данные в "items"


    def do_GET(self):
        """
        Наполняем get запрос функционалом
        :return: None
        """
        self._defining_status()
        self._fill_base_dict()
        self._set_headers()
        self._data_send_response()
        self.wfile.write(self.response_data)


    def do_POST(self):
        """
        Наполняем post запрос функционалом
        :return:
        """
        self._defining_status()
        self._fill_base_dict()
        self._get_post_data()
        self._get_dict()

        """"внедрить проверку"""
        print("post_data_dict", self.post_data_dict)
        self.error.value = self.post_data_dict

        # self._post_data_validation()

        # self._get_result_converter()

        self._set_headers()
        self._data_send_response()
        self.wfile.write(self.response_data)


class Server:
    _SERVER_CLASS = SimpleHandler
    _SERVER_ADDRESS = ('', 8000)

    def __init__(self):
        server = HTTPServer(Server._SERVER_ADDRESS, Server._SERVER_CLASS)
        try:
            print(
                f"(START) Serving HTTP on {server.server_address[0]} port {server.server_port} (http://{server.server_address[0]}:{server.server_port}/)")
            server.serve_forever()
        except KeyboardInterrupt:
            print(
                f"(STOP) Serving HTTP on {server.server_address[0]} port {server.server_port} (http://{server.server_address[0]}:{server.server_port}/)")
            server.server_close()


if __name__ == '__main__':
    server = Server()
