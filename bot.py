import os
import json
from dotenv import load_dotenv
from telegram.ext import CommandHandler,Application,CallbackQueryHandler
from fpl_analysis import best_by_position
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
from fpl_analysis import find_player_by_name,difficulty_map,position_map


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

#داله المقارنه
async def compare(update,context):
    if len(context.args)!=2:
        await update.message.reply_text("Enter to player first")
        return
    player_1=find_player_by_name(context.args[0])
    player_2=find_player_by_name(context.args[1])
    if player_1 is None or player_2 is None:
        await update.message.reply_text("The one of player is not found")
        return
    text= f'{player_1["web_name"]} \t {player_2["web_name"]} \n  ${player_1["now_cost"]/10}m \t ${player_2["now_cost"]/10}m \n {player_1["total_points"]}pts \t {player_2["total_points"]}pts \n{position_map[player_1["element_type"]]} \t {position_map[player_2["element_type"]]}\n{player_1["minutes"]}min \t {player_2["minutes"]}min \n{difficulty_map[player_1["team"]]:.2f} \t {difficulty_map[player_2["team"]]:.2f} \n'
    await update.message.reply_text(text)

#التشكليه المفضله
#dictionary فيه مراكز والاعداد المطلوبه

#اتكد من وجود الملف لو موجود اقرا منه
def load_teams():
    if os.path.exists("teams.json"):
        with open("teams.json","r")as file:
            loaded_data=json.load(file)
        return loaded_data
    else:
        a={}
        return a
#داله الكتابه
def save_teams(teams_data):
    with open("teams.json","w") as file:
        json.dump(teams_data,file)  
# داله التي في تليجرام
async def save_team(update,context):
    if len(context.args)!=15:
        await update.message.reply_text("it should to enter 15 player")
        return
    listplayer=[]
    for player_name in context.args:
        listplayer.append(player_name.upper())
    if len(listplayer)!=len(set(listplayer)):
        await update.message.reply_text(f"Duplicate player found")
        return
    required={'DEF':5,'GKP':2,'MID':5,'FWD':3}
    counts={'DEF':0,'GKP':0,'MID':0,'FWD':0}
    for name in context.args:
        player=find_player_by_name(name)
        if player is None:
            await update.message.reply_text(f"Player not found: {name}")
            return
        pos=position_map[player["element_type"]]
        counts[pos]+=1
    if counts!=required:
        await update.message.reply_text(f"should have {required},you entered {counts}")
        return
    user_id=str(update.effective_user.id)
    teams=load_teams()
    teams[user_id]=context.args
    save_teams(teams)
    await update.message.reply_text("Your team has been saved.")
#عرض الفريق
async def show_team(update,context):
    team=load_teams()
    user_id=str(update.effective_user.id)
    if user_id not in team:
        await update.message.reply_text("unavailable")
        return
    result=""
    for name in team[user_id]:
        player=find_player_by_name(name)
        if player is None:
            continue
        result+= f'{player["web_name"]} - ${player["now_cost"]/10}m - {position_map[player["element_type"]]} - {player["total_points"]}pts - {player["minutes"]}min - {difficulty_map[player["team"]]:.2f}\n'
    await update.message.reply_text(result)

app = Application.builder().token(token).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("best",best))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(CommandHandler("compare",compare))
app.add_handler(CommandHandler("save_team",save_team))
app.add_handler(CommandHandler("show_team",show_team))
app.run_polling()