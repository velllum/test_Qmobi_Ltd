


class ServerError(Exception):

    dic = {
    "Валюта_запроса": "",
    "Сумма_запроса": []
}

    dic_status = {
        "status": {
            "code": 200,
            "description": "Request fulfilled, document follows",
            "enum_name": "OK"
        }
    }



    def __init__(self):

        self.value = ServerError.dic
        self.status = ServerError.dic_status

        self.error_message = dict()
        self.text = str()


    def get_status(self):
        if self.error_message:
            self.status["status"] = self.error_message

    def _str_check_error(self, value):
        try:
            value_ = value.upper()
            if value_ != 'RUB' and value_ != 'USD':
                print("not")
                self.error_message["error_message"] = "Укажите валюту правильно 'RUB' или 'USD'"
        except Exception as e:
            print(e)


    def _num_check_error(self, value):
        try:

            if type(value) != int:
                self.error_message["error_message"] = "Введите число"

            elif value <= 0:
                print("not1")
                self.error_message["error_message"] = "Указанное число меньше ноля, или ноль"

        except Exception as e:
            print(e)




        # if not isinstance(value, str):
        #     self.error_message["error_message"] = "Вы ввели число введите пожалуйста текст"
        #
        # elif not isinstance(value, dict):
        #     self.error_message["error_message"] = "Вы ввели число введите пожалуйста текст"
        #
        # elif not isinstance(value, set):
        #     self.error_message["error_message"] = "Вы ввели число введите пожалуйста текст"


    # def _num_check_error(self, value):
    #     if not isinstance(value, int):
    #         self.error_message["error_message"] = "Вы ввели число введите пожалуйста текст"
    #
    #     elif value < 0:
    #         self.error_message["error_message"] = "Вы ввели число введите пожалуйста текст"


    # @property
    # def check_errors(self):
    #     return self.error_message
    #
    #
    # @check_errors.setter
    # def check_errors(self, value):
    #     self.value = value
    #     print(self.value)
    #     self._post_data_validation()

    def  run(self):
        self._str_check_error(self.dic["Валюта_запроса"])
        self._num_check_error(self.dic["Сумма_запроса"])
        self.get_status()



if __name__ == '__main__':
    error = ServerError()
    error.run()

    print(error.status)




# ser = ServerError()
# ser._post_data_validation()



# a = input("Input positive integer: ")
#
# try:
#     a = int(a)
#     if a < 0:
#         raise ServerError("You give negative!")
# except ValueError:
#     print("Error type of value!")
# except ServerError as mr:
#     print(mr)
# else:
#     print(a)