import json
import time
import requests
import base64
from PIL import Image
from io import BytesIO
from config import *

class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url.rstrip('/')  # Убираем лишний слэш, если он есть
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(f"{self.URL}/key/api/v1/models", headers=self.AUTH_HEADERS)
        if response.status_code != 200:
            raise ValueError(f"Ошибка запроса модели: {response.status_code}, {response.text}")
        
        data = response.json()
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("API не вернул доступных моделей.")
        
        return data[0].get('id', None)  # Проверяем, есть ли ключ 'id'

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {"query": prompt}
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        
        response = requests.post(f"{self.URL}/key/api/v1/text2image/run", headers=self.AUTH_HEADERS, files=data)
        if response.status_code != 200:
            raise ValueError(f"Ошибка генерации изображения: {response.status_code}, {response.text}")
        
        data = response.json()
        return data.get('uuid', None)

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(f"{self.URL}/key/api/v1/text2image/status/{request_id}", headers=self.AUTH_HEADERS)
            if response.status_code != 200:
                raise ValueError(f"Ошибка проверки статуса: {response.status_code}, {response.text}")
            
            data = response.json()
            if data.get('status') == 'DONE':
                return data.get('images', [])
            
            attempts -= 1
            time.sleep(delay)
        
        raise TimeoutError("Генерация изображения заняла слишком много времени.")

    def save_image(self, base64_string, file_path):
        try:
            decoded_data = base64.b64decode(base64_string)
            image = Image.open(BytesIO(decoded_data))
            image.save(file_path)
            print(f'Изображение сохранено в {file_path}')
        except Exception as e:
            raise ValueError(f"Ошибка сохранения изображения: {e}")

if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    if model_id:
        uuid = api.generate("Пушистый кот в очках", model_id)
        if uuid:
            images = api.check_generation(uuid)
            if images:
                api.save_image(images[0], 'decoded_image.jpg')

