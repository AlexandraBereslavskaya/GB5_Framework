class Request:

    @staticmethod
    def parse_input_data(data: str):
        parsed_result = {}
        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split("=")
                parsed_result[key] = value
        return parsed_result


class GetRequests(Request):

    @staticmethod
    def get_params(environ):
        query_str = environ['QUERY_STRING']
        params = GetRequests.parse_input_data(query_str)
        return params


class PostRequests(Request):

    def get_params(self, environ):
        # получили данные
        data = self.get_wsgi_input_data(environ)
        # распарсили их
        data = self.parse_wsgi_input_data(data)
        # вернули получившийся словарь
        return data

    @staticmethod
    def get_wsgi_input_data(environ):
        data_content_length = environ.get('CONTENT_LENGTH')
        if data_content_length:
            data = environ['wsgi.input'].read(int(data_content_length))
        else:
            data = b''
        return data

    def parse_wsgi_input_data(self, data: bytes):
        parsed_data = {}
        if data:
            parsed_data = self.parse_input_data(data.decode(encoding='UTF-8'))
        return parsed_data
