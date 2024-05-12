from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import ReplyKeyboardMarkup, KeyboardButton
import psycopg2
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
secret_token = os.getenv('TOKEN')

DATABASE_URL = os.getenv('DATABASE_URL')


def add_task(user_id, description):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tasks (user_id, description) VALUES (%s, %s)",
                        (user_id, description))
            conn.commit()


def get_tasks(user_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT description FROM tasks WHERE user_id = %s", (user_id,))
            tasks = cur.fetchall()
    return tasks


def start(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("/tsk")]], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет! Используйте команду /add <задача> для добавления задачи. '
             'Нажмите на кнопку /tsk для просмотра ваших задач.',
        reply_markup=reply_markup
    )


def add(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    chat = update.effective_chat
    task_description = ' '.join(context.args)
    if task_description:
        add_task(user_id, task_description)
        context.bot.send_message(
            chat_id=chat.id,
            text='Задача добавлена!'
        )
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text='Пожалуйста, введите описание задачи после команды /add.'
        )


def tsk(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    user_id = update.effective_user.id
    tasks = get_tasks(user_id)
    if tasks:
        context.bot.send_message(
            chat_id=chat.id,
            text='\n'.join(f"{index + 1}. {description[0]}" for index, description in enumerate(tasks))
        )
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text='Список задач пуст.'
        )


def main():
    updater = Updater(secret_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add, pass_args=True))
    dp.add_handler(CommandHandler("tsk", tsk))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
