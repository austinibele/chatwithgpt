# Project Name

## Introduction

This repo contains code that lets you build an interactive ChatBot, which you can actually talk too, through a Python GUI.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/austinibele/chatwithgpt.git
   ```

2. Navigate to the project directory:

   ```bash
   cd chatwithgpt
   ```

3. Replace `your_open_api_key` in src/chatbot.py with your actual Open API key, and `path_to_your_google_credentials.json` in src/transcribe.py and src/text_to_speech.py with the path to your Google Application Credentials file.

4. Start the service by running:
   ```python
   python -m src.main
   ```

## Usage

1. Press "Record" to begin recording your message.
2. Press "Stop" to end recording your message.
3. Press "Send" to send transcribe your message with Google's Speech API, send the transcription to ChatGPT (davinci-003), convert ChatGPT's response to an audiofile with Google's Speech API, and play the audiofile through your system speakers.


## License

Apache 2.0

## Contact

austin.ibele@gmail.com
