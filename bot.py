import logging
import re
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import database as db
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def get_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("Услуги фирмы")],
        [KeyboardButton("Оставить заявку")],
        [KeyboardButton("Мои заявки")],
        [KeyboardButton("Дашборд")]
    ], resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Здравствуйте, {user.first_name}! Я бот клиентского сервиса.\nВыберите действие:",
        reply_markup=get_keyboard()
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text == "Услуги фирмы":
        services = db.get_services()
        msg = "Наши услуги:\n\n"
        for s in services:
            msg += f"ID: {s[0]} | {s[1]}\nКатегория: {s[2]}\nСтоимость: от {s[3]} руб.\n\n"
        await update.message.reply_text(msg)

    elif text == "Оставить заявку":
        services = db.get_services()
        keys = [[KeyboardButton(f"Заказать: {s[1]} (ID: {s[0]})")] for s in services]
        keys.append([KeyboardButton("Отмена")])
        await update.message.reply_text(
            "Какую услугу вы хотите заказать?",
            reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True, one_time_keyboard=True)
        )

    elif text.startswith("Заказать:"):
        match = re.search(r'ID: (\d+)', text)
        if match:
            service_id = int(match.group(1))
            req_id = db.create_request(user.id, user.full_name or "Клиент", service_id)
            await update.message.reply_text(
                f"Заявка №{req_id} успешно создана! Менеджер скоро свяжется с вами.",
                reply_markup=get_keyboard()
            )

    elif text == "Мои заявки":
        reqs = db.get_user_requests(user.id)
        if not reqs:
            await update.message.reply_text("У вас пока нет заявок.")
            return
        msg = "Ваши последние заявки:\n\n"
        for r in reqs:
            msg += f"Заявка №{r[0]} - {r[1]}\nСтатус: {r[2]}\nДата: {r[3]}\n\n"
        await update.message.reply_text(msg)

    elif text == "Дашборд":
        await update.message.reply_text("Ссылка на аналитику для менеджеров: http://127.0.0.1:8050")

    elif text == "Отмена":
        await update.message.reply_text("Действие отменено.", reply_markup=get_keyboard())


def main():
    db.init_db()
    app = Application.builder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()


if __name__ == '__main__':
    main()