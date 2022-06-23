import logging
import openai
import json

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

from mtranslate import translate


keys = json.load(open('keys.json'))

openai.api_key = keys['goose']
openai.api_base = 'https://api.goose.ai/v1'


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Я самый умный бот на планете Земля!')

async def echo(update: Update, context: ContextTypes):
    text = translate(update.message.text, 'en')

    completion = openai.Completion.create(
    engine='gpt-neo-20b',
    prompt=text,
    max_tokens=128,
    stream=False)

    text = completion.choices[0].text

    ru_trans = translate(text, 'ru')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ru_trans)


if __name__ == '__main__':
    application = ApplicationBuilder().token(keys['telegram']).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    
    application.run_polling(stop_signals=None)
