import codecs
import json

from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler

from parse import Parse



# class Server:
#     def __init__(self):
#         server = HTTPServer(('', 8080), SimpleHandler)
#         server.serve_forever()


class SimpleHandler(BaseHTTPRequestHandler):

    kod = None
    message = None
    description = None
    status = HTTPStatus

    json_data = None
    post_data = None
    pars = Parse()

    dic = dict()
    # fields_status = dict()
    fields_items = dict(
            Валюта_запроса="Укажите USD или RUB",
            Сумма_запроса=0,
            Валюта_ответа="???",
            Сумма_ответа=0,
        )


    """Заполнить поля вывода статуса сервера"""
    def _fields_status(self):
        # self.fields_status = dict(
        return dict(
            status=dict(
                description=self.status.description,
                enum_name=self.status.phrase,
                code=self.status.value,
            )
        )


    # """Заполнить поля вывода данных конвертора сервера"""
    # def _fields_items(self):
    #     # self.fields_items = dict(
    #     return dict(
    #         Валюта_запроса="Укажите USD или RUB",
    #         Сумма_запроса=0,
    #         Валюта_ответа="???",
    #         Сумма_ответа=0,
    #     )


    """Создаем словарь полей с проверкой на ошибку"""
    def _make_dict(self):
        if self.status != 200:
            self.dic["error"] = self._fields_status()
        else:
            self.dic = self._fields_status()
            self.dic["status"]["items"] = self.fields_items


    """Проверка ошибки"""
    def _is_error(self):
        if self.command == "POST" and self.path != "/":
            print(self.command)
            self.status = HTTPStatus.NOT_IMPLEMENTED
        elif self.path != "/":
            self.status = HTTPStatus.NOT_FOUND
            print("GET",self.command)
        else:
            self.status = HTTPStatus.OK


    """Добавляем запрос"""
    def _set_headers(self):
        self._is_error()
        self._make_dict()
        self.send_response(self.status.value)
        self.send_header('Content-type', 'application/json')
        self.end_headers()


    """Конвертируем словарь в json массив"""
    def _get_json(self):
        json_data = json.dumps(self.dic, sort_keys=True, indent=4)
        json_data = codecs.decode(json_data, 'unicode_escape')
        self.json_data = bytes(json_data, 'utf8')


    """Получаем данные с post запроса"""
    def _get_post_data(self):
        content_length = int(self.headers['Content-Length'])
        self.post_data = self.rfile.read(content_length)


    """Конвертируем json в словарь"""
    def _get_dict(self):
        post_data = self.post_data.decode("utf8")
        self.dic_data= dict(json.loads(post_data))


    """get запроса"""
    def do_GET(self):
        self._set_headers()
        self._get_json()
        self.wfile.write(self.json_data)


    """post запроса"""
    def do_POST(self):
        self._get_post_data()
        self._get_dict()

        """Переименовать пременные ближе к челевеко понятным"""
        self.pars.fields = self.dic_data # передаем данные в парсер
        self.dic_data.update(self.pars.fields) # расширяем данными из парсера
        self.fields_items = self.dic_data # переопределяем данные а "items"


        self._set_headers()
        self._get_json()
        self.wfile.write(self.json_data)



def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)

    try:
        print(f"(START) Serving HTTP on {httpd.server_address[0]} port {httpd.server_port} (http://{httpd.server_address[0]}:{httpd.server_port}/)")
        httpd.serve_forever()

    except KeyboardInterrupt:
        print(f"(STOP) Serving HTTP on {httpd.server_address[0]} port {httpd.server_port} (http://{httpd.server_address[0]}:{httpd.server_port}/)")
        httpd.server_close()


if __name__ == '__main__':
    run(handler_class=SimpleHandler)