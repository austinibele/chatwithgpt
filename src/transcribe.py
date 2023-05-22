import os
import io
from google.cloud import speech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "path_to_your_google_credentials.json"

config = speech.RecognitionConfig(
    language_code="en",
    encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
)
config.enable_automatic_punctuation = True


def transcribe(
) -> speech.RecognizeResponse:
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = "tmp/recording.wav"

    # Loads the audio into memory
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

    # Synchronous speech recognition request
    response = client.recognize(config=config, audio=audio)
    response_text = response.results[0].alternatives[0].transcript
    return response_text

