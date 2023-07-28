import os
from typing import Any, Literal

import requests
from dotenv import load_dotenv


def main():
    global translator_endpoint
    global cog_key
    global cog_region

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_key: str | None = os.getenv('COG_SERVICE_KEY')
        cog_region: str | None = os.getenv('COG_SERVICE_REGION')
        translator_endpoint: Literal[''] = \
            'https://api.cognitive.microsofttranslator.com'

        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name),
                        encoding='utf8').read()
            print('\n' + text)

            # Detect the language
            language = GetLanguage(text)
            print('Language:', language)

            # Translate if not already English
            if language != 'en':
                translation: Literal[''] = Translate(text, language)
                print("\nTranslation:\n{}".format(translation))

    except Exception as ex:
        print(ex)


def GetLanguage(text) -> Any:
    # Default language is English
    language = 'en'

    # Use the Translator detect function
    path = '/detect'
    url = translator_endpoint + path

    # Build the request
    params: dict[str, str] = {
        'api-version': '3.0'
    }

    headers: dict[str, Any] = {
        'Ocp-Apim-Subscription-Key': cog_key,
        'Ocp-Apim-Subscription-Region': cog_region,
        'Content-type': 'application/json'
    }

    body: list[dict[str, Any]] = [{
        'text': text
    }]

    # Send the request and get response
    request: requests.Response = \
        requests.post(url, params=params, headers=headers, json=body)
    response: Any = request.json()

    # Parse JSON array and get language
    language: Any = response[0]["language"]

    # Return the language
    return language


def Translate(text, source_language) -> Literal['']:
    translation: Literal[''] = ''

    # Use the Translator translate function
    path = '/translate'
    url = translator_endpoint + path

    # Build the request
    params: dict[str, Any] = {
        'api-version': '3.0',
        'from': source_language,
        'to': ['en']
    }

    headers: dict[str, Any] = {
        'Ocp-Apim-Subscription-Key': cog_key,
        'Ocp-Apim-Subscription-Region': cog_region,
        'Content-type': 'application/json'
    }

    body: list[dict[str, Any]] = [{
        'text': text
    }]

    # Send the request and get response
    request: requests.Response = \
        requests.post(url, params=params, headers=headers, json=body)
    response: Any = request.json()

    # Parse JSON array and get translation
    translation = response[0]["translations"][0]["text"]
    # Return the translation
    return translation


if __name__ == "__main__":
    main()
