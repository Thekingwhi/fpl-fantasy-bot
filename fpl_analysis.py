import requests

# 1. جلب البيانات من API وتحويلها لـ JSON
##الخاص بالاعب
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data=response.json()
print(response.status_code)
##الخاص بالمباريات
fixtures_url ="https://fantasy.premierleague.com/api/fixtures/"
fixtures_response = requests.get(fixtures_url)
fixtures_data=fixtures_response.json()

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


### الخاص بصعوبه
#1 الجولات الغير ملعوبه
upcoming_fixtures=[]
for match in fixtures_data:
    if not match["finished"]:
        upcoming_fixtures.append(match)

#2 ترتيب المباريات لكل فريق 
def get_team_fixtures(team_id):
    result=[]
    for match in upcoming_fixtures:
        if team_id==match["team_a"] or team_id==match["team_h"]:
            result.append(match)
    result_sorted=sorted(result,key=lambda match:match["event"],reverse=False)
    return result_sorted

# تحديد الصعوبه عل ضيف او مستضيف 3
def get_difficulty_for_team(match, team_id):
    if team_id == match["team_a"]:
        return match["team_a_difficulty"]
    else:
         return match["team_h_difficulty"]

# تحديد متوسط الصعوبه 4
def get_average_difficulty(team_id):
    fixtures_team=get_team_fixtures(team_id)
    difficulty_list=[]
    for difficulty in fixtures_team[0:1]:
        difficulty_list.append(get_difficulty_for_team(difficulty,team_id))
    match=sum(difficulty_list)/len(difficulty_list)
    return match

# 5 map الصعوبه للاعبين من نفس الفريق
difficulty_map={}
for id in range(1,21):
    difficulty_map[id]=get_average_difficulty(id)



# 5. دالة لعرض أفضل اللاعبين حسب المركز
def best_by_position(pos):
    i=0
    result=""
    for player in ppm:
        if position_map[player["element_type"]]==pos:
            i+=1
            result+= f'{i} - {player["web_name"]} - ${player["now_cost"]/10}m - {position_map[player["element_type"]]} - {player["total_points"]}pts - {player["minutes"]}min - {difficulty_map[player["team"]]:.2f}\n'
            if i>=10:
                return result

