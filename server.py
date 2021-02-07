import codecs
import json

from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler

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

        self.post_request_data = bytes()
        self.response_data = bytes()
        self.base_data = dict()
        self.post_data_dict = dict()

        self.status = HTTPStatus.OK
        self.item_field = SimpleHandler._DEFAULT_FIELDS_ITEMS


        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)


    """Заполнить поля вывода статуса сервера"""
    @property
    def status_fields(self):
        return dict(
                status=dict(
                    description=self.status.description,
                    enum_name=self.status.phrase,
                    code=self.status.value,
                )
            )


    @status_fields.setter
    def status_fields(self, state_field):
        self.state_field = state_field


    """Получить поля с данными конвертера"""
    @property
    def items_fields(self):
        return self.item_field


    """Собрать поля с данными конвертера"""
    @items_fields.setter
    def items_fields(self, dic):
        self.item_field = dic


    """Проверка на ошибки сервера"""
    def _is_error(self):
        if self.command == "POST" and self.path != "/":
            self.status = HTTPStatus.NOT_IMPLEMENTED
        elif self.path != "/":
            self.status = HTTPStatus.NOT_FOUND



    """Создаем словарь полей с проверкой на ошибку"""
    def _make_dict(self):
        if self.status != 200:
            self.base_data["error"] = self.status_fields
        else:
            self.base_data = self.status_fields
            self.base_data["status"]["items"] = self.items_fields


    """Добавляем запрос"""
    def _set_headers(self):
        self._is_error()
        self._make_dict()
        self.send_response(self.status.value)
        self.send_header('Content-type', 'application/json')
        self.end_headers()


    """Конвертируем словарь в json массив"""
    def _get_json(self):
        data = json.dumps(self.base_data, sort_keys=True, indent=4)
        data = codecs.decode(data, 'unicode_escape')
        self.response_data = bytes(data, 'utf8')


    """Получаем данные с post запроса"""
    def _get_post_data(self):
        content_length = int(self.headers['Content-Length'])
        self.post_request_data = self.rfile.read(content_length)


    """Конвертируем полученные post данные в словарь"""
    def _get_dict(self):
        data = self.post_request_data.decode("utf8")
        print("data", type(data),data)
        self.post_data_dict = dict(json.loads(data))
        print(type(self.post_data_dict["Валюта_запроса"])) # isinstance


    """Проверка отправленных данных на сервер"""
    def _post_data_validation(self):
        text = self.post_data_dict["Валюта_запроса"]
        if not isinstance(text, str):
            self.status_fields = "Вы ввели число введите пожалуйста текст"


    """Результат работы конвертора"""
    def _get_result_converter(self):
        self.pars.fields = self.post_data_dict  # передаем данные в парсер
        self.post_data_dict.update(self.pars.fields)  # расширяем данными из парсера
        self.items_fields = self.post_data_dict  # переопределяем данные а "items"


    """get запрос"""
    def do_GET(self):
        self._set_headers()
        self._get_json()
        self.wfile.write(self.response_data)


    """post запрос"""
    def do_POST(self):
        self._get_post_data()
        self._get_dict()

        self._post_data_validation()

        # self._get_result_converter()

        self._set_headers()
        self._get_json()
        self.wfile.write(self.response_data)




class Server:

    _SERVER_CLASS = SimpleHandler
    _SERVER_ADDRESS = ('', 8000)

    def __init__(self):
        server = HTTPServer(Server._SERVER_ADDRESS, Server._SERVER_CLASS)
        try:
            print(f"(START) Serving HTTP on {server.server_address[0]} port {server.server_port} (http://{server.server_address[0]}:{server.server_port}/)")
            server.serve_forever()
        except KeyboardInterrupt:
            print(f"(STOP) Serving HTTP on {server.server_address[0]} port {server.server_port} (http://{server.server_address[0]}:{server.server_port}/)")
            server.server_close()



if __name__ == '__main__':
    server = Server()
