import telebot
import handlers
import config
from config import bot

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)