import openai
from telegram import Update, Bot
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, Filters
import sys, os
import json

# insert corresponding tokens in terminal like that: python3 tgchatGPT.py token1 token2 IDS_path
openai.api_key, TOKEN, IDS_path = sys.argv[1:4]

# CONSTS
DEFAULT_DICT    = {'state':'chat', 'chat':'', 'img':None}
MEMORY_REQUESTS = 5  
MYID, HERID = 283460642, 284672038
GODS = {MYID : "к вашим услугам, господин", HERID : "пупсопривив"}

# MEMORY dict to save states of users to switch img/chat regimes
# {id1:{'chat' : prompt1+pronpt2+..., 'img' : prompt, 'state' : 'img'}, id2:..., ...}
MEMORY = {}

# IDS
if not os.path.exists(IDS_path):
  with open(IDS_path, 'w+') as fp:
    json.dump({}, fp)
with open(IDS_path, 'r') as fp:
  IDS = json.load(fp)

# GPT chat api implementation
def GPTchat(prompt):
  return openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": prompt},
          ],)['choices'][0]['message']['content']

# GPT img api implementation
def GPTimg(prompt):
  return openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024")['data'][0]['url']

# /start command
def start_command(update: Update, context: CallbackContext) -> None:
  chat_id  = update.message.chat_id
  username = update.message.from_user.username
  if username not in IDS:
    IDS[username] = chat_id
    with open(IDS_path, 'w+') as fp:
      json.dump(IDS, fp)
  if chat_id in GODS:
    update.message.reply_text(GODS[chat_id])
  else:
    update.message.reply_text('ну, чего тебе?')
  MEMORY[chat_id] = DEFAULT_DICT.copy()

# /img command
def img(update: Update, context: CallbackContext) -> None:
  chat_id = update.message.chat_id
  if chat_id not in MEMORY:
    MEMORY[chat_id] = DEFAULT_DICT.copy()
  MEMORY[chat_id]['state'] = 'img'
  update.message.reply_text('рисоватб: ON')

# /chat command
def chat(update: Update, context: CallbackContext) -> None:
  chat_id = update.message.chat_id
  if chat_id not in MEMORY:
    MEMORY[chat_id] = DEFAULT_DICT.copy()
  MEMORY[chat_id]['state'] = 'chat'
  update.message.reply_text('чатб: ON')

# handler for any text
def handleGPT(update: Update, context: CallbackContext):
  try:
    chat_id = update.message.chat_id
    prompt  = update.message.text.lower()
    if chat_id not in MEMORY:
      MEMORY[chat_id] = DEFAULT_DICT.copy()

    # using GPT image api
    if MEMORY[chat_id]['state'] == 'img':
      image = GPTimg(prompt)
      MEMORY[chat_id]['img'] = prompt +' -> '+ image
      update.message.reply_text(image)

    # using GPT chat api
    else:
      if len(MEMORY[chat_id]['chat'].split('\n\n'))>=2*MEMORY_REQUESTS: # max context cap
        MEMORY[chat_id]['chat'] = ''
      MEMORY[chat_id]['chat'] += prompt
      answer = GPTchat(MEMORY[chat_id]['chat'])
      MEMORY[chat_id]['chat'] += '\n\n' + answer + '\n\n'
      update.message.reply_text(answer)

  except Exception as e:
    print(e)
    update.message.reply_text('я сломалосб')

# auxikiary staff
def void(update: Update, context: CallbackContext) -> None:
  if update.message.chat_id in GODS:
    global MEMORY
    MEMORY = {}
    update.message.reply_text('души свободны')
  else:
    update.message.reply_text('ты не обладаешь этой силой')
def get(update: Update, context: CallbackContext) -> None:
  if update.message.chat_id in GODS:
    update.message.reply_text("\n————————————————————\n".join(
      [f"{n+1}) {IDS[key]}\n\n chat: {MEMORY[key]['chat']} - - - \n img: {MEMORY[key]['img']}" 
        for n,key in enumerate(MEMORY)]))
  else:
    update.message.reply_text('ты не обладаешь этой силой')
def send(update: Update, context: CallbackContext) -> None:
  try:
    if update.message.chat_id in GODS:
      _, username, msg = update.message.text.split(' ', 2)
      Bot(token=TOKEN).send_message(chat_id = IDS[username], text = msg)
    else:
      update.message.reply_text('ты не обладаешь этой силой')
  except:
    pass

# put all together and start pooling
handlers = [
  CommandHandler('start', start_command),
  CommandHandler('chat', chat),
  CommandHandler('img', img),
  CommandHandler('void', void),
  CommandHandler('get', get),
  CommandHandler('send', send),
  MessageHandler(Filters.all, handleGPT),
]
updater = Updater(TOKEN, workers=100)
for handler in handlers:
  updater.dispatcher.add_handler(handler)
updater.start_polling()
print('Start bot')
updater.idle()