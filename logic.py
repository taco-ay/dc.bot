from config import API_KEY, SECRET_KEY
import json
import time

import requests
import PIL #pip install Pillow
from PIL import Image
import base64 
import io


class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, negatif = "",images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "negativePromptDecoder": negatif,
            "generateParams": {
                "query": prompt
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)

def foto_uret(prompt, negatif = ""):
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    pipeline_id = api.get_pipeline()
    uuid = api.generate(f"{prompt}", pipeline_id, f"{negatif}")
    files = api.check_generation(uuid)
    return files[0]


def foto_cevir(base64_str, output_path):
    image_str = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(image_str))
    image = image.convert("RGB")
    image.save(output_path, "jpeg")


if __name__ == '__main__':
    foto_cevir(foto_uret("taco", "angry"), "taco.jpeg")
