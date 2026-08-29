import os
from dotenv import load_dotenv
from telegram.ext import CommandHandler,Application,CallbackQueryHandler
from fpl_analysis import best_by_position
from telegram import InlineKeyboardMarkup,InlineKeyboardButton

load_dotenv()
token=os.getenv("BOT_TOKEN")
print(type(token))
print(len(token))

async def start(update,context):
    button=InlineKeyboardButton("Forwards",callback_data="FWD")
    keyboard=InlineKeyboardMarkup([[button]])
    await update.message.reply_text("helloooo!",reply_markup=keyboard)

async def button_handler(update,context):
    query=update.callback_query
    await query.answer()

    pos=query.data
    text=best_by_position(pos)
    await query.edit_message_text(text)

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