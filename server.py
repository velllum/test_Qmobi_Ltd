import codecs
import json

from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    dic = {}
    kod = None
    message = None
    description = None
    json_data = None
    post_data = None
    status = HTTPStatus



    """Заполнить поля статуса сервера"""
    def _fields_status(self):
        return {
            "status": {
                "description": self.status.description,
                "enum_name": self.status.phrase,
                "code": self.status.value,
            }
        }

    """Заполнить поля данные, по умолчанию равные нолю"""
    def _fields_items(self):
        return {
            "Результат": 0,
            "Сумма_запроса": "Укажите сумму",
            "Валюта": "Укажите USD или RUB",
        }


    """Создаем словарь полей с проверкой на ошибку"""
    def _make_dict(self):
        if self.status != 200:
            self.dic["error"] = self._fields_status()
        else:
            self.dic = self._fields_status()
            self.dic["status"]["items"] = self._fields_items()


    """Проверка ошибки"""
    def _is_error(self):
        if self.command == "POST" and self.path != "/":
            print(self.command, self.path)
            self.status = HTTPStatus.NOT_IMPLEMENTED

        elif self.path != "/":
            self.status = HTTPStatus.NOT_FOUND
            print("GET",self.command)

        else:
            self.status = HTTPStatus.OK

        self._make_dict()


    """Добавляем запрос"""
    def _set_headers(self):
        self._is_error()
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
        self._set_headers()
        self._get_post_data()
        self._get_dict()

        #==============================
        # Обрабатываем полученные данные
        print(self.dic)
        print("dic_data", self.dic_data)
        #================================

        # создать парсер для обработки

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
    run(handler_class=SimpleHTTPRequestHandler)