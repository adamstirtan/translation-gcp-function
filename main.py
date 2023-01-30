import os
import functions_framework

from flask import jsonify
from google.cloud import translate_v2 as translate
from slack.signature import SignatureVerifier

translate_client = translate.Client()

def format_slack_message(text, translated_text, target_language, source_language):
    message = {
        'response_type': 'in_channel',
        'attachments': []
    }

    attachment = {
        'color': '#0014d1',
        'fields': []
    }

    attachment['pretext'] = 'Translation: {}'.format(text)
    attachment['text'] = translated_text

    attachment['fields'].append({
        'title': 'From',
        'value': source_language,
        'short': True
    })

    attachment['fields'].append({
        'title': 'To',
        'value': target_language,
        'short': True
    })

    message['attachments'].append(attachment)

    return message

def verify_signature(request):
    request.get_data()

    verifier = SignatureVerifier(os.environ['SLACK_SECRET'])

    if not verifier.is_valid_request(request.data, request.headers):
        raise ValueError('Invalid request/credentials.')

def make_translation_request(text, target_language, source_language):
    if (target_language == source_language):
        return text

    translation = translate_client.translate(
        text, target_language = target_language, source_language = source_language
    )

    return translation

def translate(request, target_language):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405

    #verify_signature(request)

    text = request.form['text']
    source_language = translate_client.detect_language(text)

    translation = make_translation_request(text, target_language, source_language['language'])

    slack_message = format_slack_message(
        text, translation['translatedText'], target_language, source_language['language'])

    return slack_message

@functions_framework.http
def to_french(request):
    return translate(request, 'fr')

@functions_framework.http
def to_spanish(request):
    return translate(request, 'es')

@functions_framework.http
def to_english(request):
    return translate(request, 'en')