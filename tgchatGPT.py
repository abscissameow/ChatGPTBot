import openai
from telegram import Update, Bot
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, Filters
import sys, os
import json
from copy import deepcopy

# insert corresponding tokens in terminal like that: python3 tgchatGPT.py token1 token2 IDS_path
openai.api_key, TOKEN, IDS_path = sys.argv[1:4]

# CONSTS
DEFAULT_DICT    = {'state':'chat', 'a':list(), 'q':list()}
MEMORY_REQUESTS = 7
MAX_TOKENS = 2800
MYID, HERID = 283460642, 284672038
GODS = {MYID : "к вашим услугам, господин", HERID : "пупсопривив"}

# MEMORY dict to save states of users to switch img/chat regimes and to store chat memory
MEMORY = {}

# IDS
if not os.path.exists(IDS_path):
  with open(IDS_path, 'w+') as fp:
    json.dump({}, fp)
with open(IDS_path, 'r') as fp:
  IDS = json.load(fp)
def fill(chat_id, username):
  if username not in IDS:
    IDS[str(username)] = chat_id
    IDS[str(chat_id) ] = str(username)
    with open(IDS_path, 'w+') as fp:
      json.dump(IDS, fp)
  if chat_id not in MEMORY:
    MEMORY[chat_id] = deepcopy(DEFAULT_DICT)
  
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
  fill(chat_id, update.message.from_user.username)
  if chat_id in GODS:
    update.message.reply_text(GODS[chat_id])
  else:
    update.message.reply_text('ну, чего тебе?')

# /img command
def img(update: Update, context: CallbackContext) -> None:
  chat_id  = update.message.chat_id 
  fill(chat_id, update.message.from_user.username)
  MEMORY[chat_id]['state'] = 'img'
  update.message.reply_text('рисоватб: ON')

# /chat command
def chat(update: Update, context: CallbackContext) -> None:
  chat_id = update.message.chat_id
  fill(chat_id, update.message.from_user.username)
  MEMORY[chat_id]['state'] = 'chat'
  update.message.reply_text('чатб: ON')

def _cap_memory(id):
  T = len(''.join(MEMORY[id]['q']+MEMORY[id]['a']).split())
  if len(MEMORY[id]['q']) >= MEMORY_REQUESTS or T > MAX_TOKENS:
    MEMORY[id]['a'].pop(0)
    MEMORY[id]['q'].pop(0)
    _cap_memory(id)
# handler for any text
def handleGPT(update: Update, context: CallbackContext):
  try:
    chat_id = update.message.chat_id
    msg     = update.message.text.lower()
    fill(chat_id, update.message.from_user.username)

    # using GPT image api
    if MEMORY[chat_id]['state'] == 'img':
      update.message.reply_text(GPTimg(msg))
      
    # using GPT chat api
    else:
      _cap_memory(chat_id)
      prompt = '\n'.join([i for j in zip(MEMORY[chat_id]['q'],MEMORY[chat_id]['a'])\
                            for i in j]) + '\n' + msg
      answer = GPTchat(prompt)
      MEMORY[chat_id]['q'].append(msg)
      MEMORY[chat_id]['a'].append(answer)
      update.message.reply_text(answer)

  except Exception as e:
    update.message.reply_text('я сломалосб:\n' + str(e))

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
    users = '\n'.join([IDS[str(key)]+' : '+str(len(MEMORY[key]['q'])) for key in MEMORY])
    if not users:
      update.message.reply_text('одиноко...')
    else:
      update.message.reply_text(users)
      update.message.reply_text("\n\n".join(
        [f"{n+1}) {IDS[str(key)]}\n\
        {(MEMORY[key]['q'][-1] if MEMORY[key]['q'] else None)}"[:4096//len(MEMORY)]\
        for n,key in enumerate(MEMORY)]))
  else:
    update.message.reply_text('ты не обладаешь этой силой')
def send(update: Update, context: CallbackContext) -> None:
  if update.message.chat_id in GODS:
    _, username, msg = update.message.text.split(' ', 2)
    Bot(token=TOKEN).send_message(chat_id = IDS[username], text = msg)
  else:
    update.message.reply_text('ты не обладаешь этой силой')

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