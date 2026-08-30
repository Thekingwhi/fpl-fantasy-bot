import os
from dotenv import load_dotenv
from telegram.ext import CommandHandler,Application,CallbackQueryHandler
from fpl_analysis import best_by_position
from telegram import InlineKeyboardMarkup,InlineKeyboardButton

load_dotenv()
token=os.getenv("BOT_TOKEN")
print(type(token))
print(len(token))

def build_keyboard():
    button=InlineKeyboardButton("Forwards",callback_data="FWD")
    button1=InlineKeyboardButton("Defenders",callback_data="DEF")
    button2=InlineKeyboardButton("Midfielders",callback_data="MID")
    button3=InlineKeyboardButton("Goalkeepers",callback_data="GKP")

    keyboard=InlineKeyboardMarkup([[button],[button1],[button2],[button3]])

    return keyboard

async def start(update,context):
    keyboard=build_keyboard()
    await update.message.reply_text("hellooo!",reply_markup=keyboard)

#async def position(update,context):

async def button_handler(update,context):
    query=update.callback_query
    await query.answer()

    keyboard=build_keyboard()
    pos=query.data
    text=best_by_position(pos)
    await query.edit_message_text(text,reply_markup=keyboard)

async def best(update,context):
    if len(context.args)==0:
        await update.message.reply_text("write the position")
        return
 
    pos=str(context.args[0]).upper()

    valid_positions = ["GKP", "DEF", "MID", "FWD"]
    if pos not in valid_positions:
        await update.message.reply_text("the position unavailable")
        return

    text=best_by_position(pos)
    await update.message.reply_text(text)



app = Application.builder().token(token).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("best",best))
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()