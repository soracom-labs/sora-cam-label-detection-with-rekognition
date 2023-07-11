import requests


class LineNotify(object):
    def __init__(self, token: str,
                 api_url: str = 'https://notify-api.line.me/api/notify'):
        self.token = token
        self.api_url = api_url

    def notify_to_line_with_image(self, message, image_bytes):
        """Notify the result to LINE"""
        headers = {'Authorization': 'Bearer ' + self.token}

        data = {'message': 'message: ' + message}
        files = {'imageFile': image_bytes}
        response = requests.post(
            self.api_url, headers=headers, data=data, files=files, timeout=5)
        print(response)
