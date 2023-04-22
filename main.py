""" Основной файл бота. Запускать это. """


from loader import bot
import handlers
from telebot.custom_filters import StateFilter
import utils
from loguru import logger


if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    utils.set_bot_commands.set_default_commands(bot)
    logger.info("Bot commands are set.")
    logger.success("Starting the Bot.")
    bot.infinity_polling()
    logger.info("Bot stopped.")
    