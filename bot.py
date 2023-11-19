import logging

from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

from src.config.config import Config
from src.transaction.pay import Transaction
from src.user.user import get_user_by_id
from src.type.type import bank_list_type

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# INIT
BUTTON_BANK, BUTTON_CATEGORY, BUTTON_SHOP, BUTTON_WHO, BUTTON_DESCRIPTION, BUTTON_CONSTANT, BUTTON_PRICE, BUTTON_PAYED, BUTTON_CASHBACK = range(9)

# common
START_OVER, COMPLETE, START_ROUTES, END_ROUTES = range(10, 14)

# CHANGE
CHANGE_WHO, CHANGE_BANK, CHANGE_CONSTANT, CHANGE_DESCRIPTION, CHANGE_CASHBACK, CHANGE_PAYED, CHANGE_PRICE, CHANGE_CATEGORY, CHANGE_SHOP = range(15, 24)

# bank list
TINKOFF_BANK, ALFA_BANK, SBER_BANK, OZON_BANK, YANDEX_BANK, ADD_BANK_INPUT = range(6)

def get_bank_name_by_id(bank_id: int) -> bank_list_type | None:
    match bank_id:
        case 0:
            return "Тинек"
        case 1:
            return "Альфа"
        case 2:
            return "Сбер"
        case 3:
            return "Озон"
        case 4:
            return "Яндекс"
        case _:
            return None


END = ConversationHandler.END

back_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text="Назад", callback_data=str(START_OVER)),
    ],
])

pay_keyboard = InlineKeyboardMarkup([
        # [
        #     InlineKeyboardButton(text="Назад", callback_data=str(TO_GENERAL_MENU)),
        #    TO_PAYED_MENU
        # ],
        [
            InlineKeyboardButton(text="Банк", callback_data=str(BUTTON_BANK)),
            InlineKeyboardButton(text="Категория", callback_data=str(BUTTON_CATEGORY)),
        ],
        [
            InlineKeyboardButton(text="Магазин", callback_data=str(BUTTON_SHOP)),
            InlineKeyboardButton(text="Кому", callback_data=str(BUTTON_WHO)),
        ],
        [
            InlineKeyboardButton(text="Описание", callback_data=str(BUTTON_DESCRIPTION)),
            InlineKeyboardButton(text=f"Постоянная", callback_data=str(BUTTON_CONSTANT)),
        ],
        [
            InlineKeyboardButton(text="Цена", callback_data=str(BUTTON_PRICE)),
            InlineKeyboardButton(text="Заплачено", callback_data=str(BUTTON_PAYED)),
            InlineKeyboardButton(text="Кешбек", callback_data=str(BUTTON_CASHBACK)),
        ],
        [
            InlineKeyboardButton(text="Готово", callback_data=str(COMPLETE)),
        ]
    ])

class Pay():
    transaction: Transaction

    async def entry_point(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = get_user_by_id(update.effective_chat.id)
        logging.error(update.effective_chat.id)
        if user != None:
            self.transaction = Transaction(user['name'], user['bank'])
            await update.message.reply_text(text=self.transaction.pretty_print(), reply_markup=pay_keyboard)
            return START_ROUTES
        else:
            raise Exception('user not found')

    async def change_bank(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="Тинек", callback_data=str(TINKOFF_BANK)),
                InlineKeyboardButton(text="Альфа", callback_data=str(ALFA_BANK)),
                InlineKeyboardButton(text="Сбер", callback_data=str(SBER_BANK)),
            ],
            [
                InlineKeyboardButton(text="Озон", callback_data=str(OZON_BANK)),
                InlineKeyboardButton(text="Яндекс", callback_data=str(YANDEX_BANK)),
            ],
            # [
            #     InlineKeyboardButton(text="Добавить еще банк", callback_data=str(ADD_BANK_INPUT)),
            # ],
            [
                InlineKeyboardButton(text="Назад", callback_data=str(START_OVER)),
            ]
        ])
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="Выбирай банк в котором совершена транзакция", reply_markup=buttons)
        return CHANGE_BANK

    async def set_bank(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bank_id = update['callback_query']['data']
        bank_name = get_bank_name_by_id(int(bank_id))
        if bank_name:
            self.transaction.change_bank(bank_name)
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(text=self.transaction.pretty_print(), reply_markup=pay_keyboard)
            return START_ROUTES
        else:
            raise Exception('bank not found')

    async def change_category(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="Введи категорию транзакции", reply_markup=back_keyboard)
        return CHANGE_CATEGORY

    async def change_shop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # buttons = [
        #     # ... some shops
        #     [
        #         InlineKeyboardButton(text="Добавить магазин", callback_data=str(ADD_SHOP)),
        #     ],
        #     [
        #         InlineKeyboardButton(text="< назад", callback_data=str(PREV_SHOPT_PAGE)),
        #         InlineKeyboardButton(text="дальше >", callback_data=str(NEXT_SHOPT_PAGE)),
        #     ]
        # ]
        # keyboard = InlineKeyboardMarkup(buttons)
        # await update.callback_query.edit_message_text(text="Выбери магазин", reply_markup=keyboard)
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="Введи название магазина", reply_markup=back_keyboard)
        return CHANGE_SHOP

    async def change_who(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="Себе", callback_data='себе'),
                InlineKeyboardButton(text="Семье", callback_data='семье'),
                InlineKeyboardButton(text="Родственникам", callback_data='родственникам'),
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data=str(START_OVER)),
            ]
        ])
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="Кому покупка? Нажми на кнопку, или введи название", reply_markup=buttons)
        return CHANGE_WHO

    async def ask_for_shop_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.transaction.change_shop(str(update.message.text).lower())
        user_data = context.user_data
        user_data[START_OVER] = True
        return await self.start_over(update, context)

    async def ask_for_category_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.transaction.change_category(str(update.message.text).lower())
        user_data = context.user_data
        user_data[START_OVER] = True
        return await self.start_over(update, context)

    async def ask_for_description_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.transaction.change_description(str(update.message.text).lower())
        user_data = context.user_data
        user_data[START_OVER] = True
        return await self.start_over(update, context)

    async def ask_for_payed_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.transaction.set_payed(int(update.message.text))
        user_data = context.user_data
        user_data[START_OVER] = True
        return await self.start_over(update, context)

    async def ask_for_cashback_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.transaction.set_cashback(int(update.message.text))
        user_data = context.user_data
        user_data[START_OVER] = True
        return await self.start_over(update, context)

    async def ask_for_price_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.transaction.set_price(int(update.message.text))
        user_data = context.user_data
        user_data[START_OVER] = True
        return await self.start_over(update, context)
    
    async def ask_for_who_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.transaction.change_who(str(update.message.text).lower())
        user_data = context.user_data
        user_data[START_OVER] = True
        return await self.start_over(update, context)

    async def change_description(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = "Введи, что было куплено"
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=back_keyboard)
        return CHANGE_DESCRIPTION

    async def change_constant(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.transaction.change_constant()
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=self.transaction.pretty_print(), reply_markup=pay_keyboard)
        return await self.start_over(update, context)

    async def change_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="Сколько была цена в магазине? (Только цифры)", reply_markup=back_keyboard)
        return CHANGE_PRICE

    async def change_payed(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="Сколько было заплачено? (Только цифры)", reply_markup=back_keyboard)
        return CHANGE_PAYED

    async def change_cashback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="Сколько кешбека дали рублей? (только цифры)", reply_markup=back_keyboard)
        return CHANGE_CASHBACK

    async def complete(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="Отлично, пока)")
        return END

    async def start_over(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.user_data.get(START_OVER):
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(text=self.transaction.pretty_print(), reply_markup=pay_keyboard)
        else:
            await update.message.reply_text(text=self.transaction.pretty_print(), reply_markup=pay_keyboard)

        context.user_data[START_OVER] = False
        return START_ROUTES


def main() -> None:
    config = Config()
    application = Application.builder().token(config.telegram_token).build()

    control = Pay()
    main_conv = ConversationHandler(
        entry_points=[
            CommandHandler('start', control.entry_point)
        ],
        states={
            START_ROUTES: [
                CallbackQueryHandler(control.change_bank, pattern=f"^{BUTTON_BANK}$"),
                CallbackQueryHandler(control.change_category, pattern=f"^{BUTTON_CATEGORY}$"),
                CallbackQueryHandler(control.change_shop, pattern=f"^{BUTTON_SHOP}$"),
                CallbackQueryHandler(control.change_who, pattern=f"^{BUTTON_WHO}$"),
                CallbackQueryHandler(control.change_description, pattern=f"^{BUTTON_DESCRIPTION}$"),
                CallbackQueryHandler(control.change_constant, pattern=f"^{BUTTON_CONSTANT}$"),
                CallbackQueryHandler(control.change_price, pattern=f"^{BUTTON_PRICE}$"),
                CallbackQueryHandler(control.change_payed, pattern=f"^{BUTTON_PAYED}$"),
                CallbackQueryHandler(control.change_cashback, pattern=f"^{BUTTON_CASHBACK}$"),

                # finalize
                CallbackQueryHandler(control.complete, pattern=f"^{COMPLETE}$"),
                CallbackQueryHandler(control.start_over, pattern=f"^{START_OVER}$"),
                CallbackQueryHandler(control.stop, pattern=f"^{END_ROUTES}$"),
            ],
            CHANGE_WHO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, control.ask_for_who_input),
                CallbackQueryHandler(control.start_over, pattern=f"^{START_OVER}$"),
            ],
            CHANGE_CATEGORY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, control.ask_for_category_input),
                CallbackQueryHandler(control.start_over, pattern=f"^{START_OVER}$"),
            ],
            CHANGE_SHOP: [
                # MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^(родственникам|себе|семье)$")), control.ask_for_shop_input),
                MessageHandler(filters.TEXT & ~filters.COMMAND, control.ask_for_shop_input),
                CallbackQueryHandler(control.start_over, pattern=f"^{START_OVER}$"),
            ],
            CHANGE_BANK: [
                CallbackQueryHandler(control.set_bank, pattern=f"^{TINKOFF_BANK}|^{ALFA_BANK}$|^{SBER_BANK}$|^{OZON_BANK}$|^{YANDEX_BANK}$"),
                CallbackQueryHandler(control.start_over, pattern=f"^{START_OVER}$"),
            ],
            CHANGE_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, control.ask_for_description_input),
                CallbackQueryHandler(control.start_over, pattern=f"^{START_OVER}$"),
            ],
            CHANGE_CASHBACK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, control.ask_for_cashback_input),
                CallbackQueryHandler(control.start_over, pattern=f"^{START_OVER}$"),
            ],
            CHANGE_PAYED: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, control.ask_for_payed_input),
                CallbackQueryHandler(control.start_over, pattern=f"^{START_OVER}$"),
            ],
            CHANGE_PRICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, control.ask_for_price_input),
                CallbackQueryHandler(control.start_over, pattern=f"^{START_OVER}$"),
            ]
        },
        fallbacks=[
            CommandHandler("stop", control.stop),
            CommandHandler('start', control.entry_point),
            # CallbackQueryHandler(control.stop, pattern=f"^{END_ROUTES}$"),
            CallbackQueryHandler(control.start_over, pattern=f"^{START_OVER}$"),
        ],
    )

    application.add_handler(main_conv)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()