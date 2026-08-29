import requests

# 1. جلب البيانات من API وتحويلها لـ JSON
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data=response.json()
print(response.status_code)

players=data["elements"]

# 2. بناء جدول ربط رقم المركز باسمه
position_map={}
for pos in data["element_types"]:
    position_map[pos["id"]]=pos["singular_name_short"]

# 3. فلترة اللاعبين حسب وقت اللعب
max_minutes=max(players,key=lambda player:player["minutes"])
min_minutes_threshold = max_minutes["minutes"]*0.5
eligible_players=[]
for player in players:
    if player["minutes"]>=min_minutes_threshold:
        eligible_players.append(player)

# 4. ترتيب اللاعبين حسب القيمة (PPM)
ppm=sorted(eligible_players,key=lambda player: player["total_points"]/(player["now_cost"]/10),reverse=True)

# 5. دالة لعرض أفضل اللاعبين حسب المركز
def best_by_position(pos):
    i=0
    result=""
    for player in ppm:
        if position_map[player["element_type"]]==pos:
            i+=1
            result+= f'{i} - {player["web_name"]} - ${player["now_cost"]/10}m - {position_map[player["element_type"]]} - {player["total_points"]}pts - {player["minutes"]}min\n'
            if i>=10:
                return result


