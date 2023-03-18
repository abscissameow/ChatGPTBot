<h1 align="center">ChatGPT Telegram Bot</h1>

This is a Python script that uses OpenAI's GPT-3 API and Telegram's Bot API to create a chatbot that can generate text, voice and images in response to user input.

#### Used AI models:
- **gpt-3.5-turbo** for chat responses generation
- **DALL·E** for pictures generation
- **whisper-1** for speech-text convertation
- **gTTS** (Google Text-to-Speech) for speech generation

## Getting Started
Install dependences using pip:
```bash
pip install openai python-telegram-bot==13.7 pydub gtts
```

To use the code, you will need to have a Telegram bot **token** and an OpenAI API **key**. Once you have these, you can insert them into the python3 tgchatGPT.py command in your terminal like this:
```php
python3 tgchatGPT.py <OpenAI API key> <Telegram Bot token>
```

## Usage
Once the script is running, you can interact with the bot using Telegram. The following commands are available:

- `/start` - Initializes the bot and provides a welcome message.
- `/chat` - Switches the bot to chat mode, where it will generate text in response to user input.
- `/img` - Switches the bot to image mode, where it will generate images in response to user input.

When the bot is in chat mode, it will attempt to generate a response to any text message it receives using OpenAI's GPT API. The bot will remember the last 7 conversation turns and will incorporate them into its response to provide context.

When the bot is in image mode, it will attempt to generate an image in response to any text message it receives using OpenAI's DALL-E API.

In addition to text messages, the bot can also handle **voice** files. If you send a voice message to the bot, it will convert it to text using OpenAI's Whisper API and then pass the text to the GPT or DALL-E API (depending on the first word spoken: **write**, **draw**, or without) to generate a response.

### P.S.
~~this README.md file was generated using ChatGPT Telegram Bot~~




