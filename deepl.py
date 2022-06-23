import requests

API_ENDPOINT = 'https://deepl.deno.dev/translate'


def translate(text, target):
    request = {
        'text': text,
        'source_lang': "auto",
        'target_lang': target,
    }
    response = requests.post(API_ENDPOINT, json=request).json()
    return response['data']
