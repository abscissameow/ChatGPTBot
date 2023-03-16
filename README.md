# A simple telegram bot using free GPT-3 API

## Used AI models:
- `gpt-3.5-turbo` for chat responses generation
- `DALL·E` for pictures generation
- `whisper-1` for speech-text convertation
- `gTTS` (Google Text-to-Speech) for speech generation

## Telegram api usage: 
```bash
python3 tgchatGPT.py token_openai token_tgBot
```
## Bot usage: 
There are two buttons for `drawing` only / `chat` only (called `рисоватб` and `чатб`)\
Bot also can handle `voice` messages: 
- If the `first word` of voice message is "`write`" then the output is in `text` format. 
- If it is "`draw`" then the output is `pic`. 
- Otherwise the output will be in `voice` format.
