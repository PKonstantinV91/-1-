import requests
import json
from pprint import pprint


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def upload(self, path, photo_file):
        """Метод загружает файл на яндекс диск"""
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        final_file = []
        for k, v in photo_file.items():
            headers = self.get_headers()
            url_ = v[0]
            path_ = f'{path}/{k}'
            params = {'path': path_, 'url': url_, 'overwrite': 'true'}
            res = requests.post(upload_url, headers=headers, params=params)
            final_file.append({'file_name': k, 'size': v[1]})

        return json.dumps(final_file)


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_photos(self, owner_id):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': owner_id, 'album_id': 'profile',
            'photo_sizes': 1, 'extended': 1, 'count': 5
        }
        res = requests.get(url, params={**self.params, **params})
        photos_list = res.json()['response']['items']
        photo_file = {}
        for i in photos_list:
            size = i['sizes'][4]
            size_type = size['type']
            photo_url = size['url']
            file_name = str(i['likes']['count']) + '.' + str(i['date'])
            photo_file.update({f'{file_name}.jpg': [photo_url, size_type]})

        return photo_file


if __name__ == '__main__':
    token = ''
    access_token = ''
    user_id = ''
    owner_id = ''
    vk = VK(access_token, user_id)
    uploader = YaUploader(token)
    photo_file = vk.users_photos(owner_id)
    pprint(uploader.upload('Фото VK', photo_file))
