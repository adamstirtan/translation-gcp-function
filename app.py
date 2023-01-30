import os
import functions_framework

from flask import jsonify
from google.cloud import translate_v2 as translate
from slack.signature import SignatureVerifier

translate_client = translate.Client()

def verify_signature(request):
    request.get_data()

    verifier = SignatureVerifier(os.environ['SLACK_SECRET'])

    if not verifier.is_valid_request(request.data, request.headers):
        raise ValueError('Invalid request/credentials.')

def make_translation_request(text, target_language, source_language):
    if (target_language == source_language):
        return text

    return translate_client.translate(
        text, target_language, source_language
    )

def translate(request, language):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405

    verify_signature(request)

    text = request.form['text']
    source_language = translate_client.detect_language(text)

    translation_response = make_translation_request(text, language, source_language)

    return jsonify(translation_response)

@functions_framework.http
def to_french(request):
    return translate(request, 'fr')

@functions_framework.http
def to_spanish(request):
    return translate(request, 'es')

@functions_framework.http
def to_english(request):
    return translate(request, 'en')