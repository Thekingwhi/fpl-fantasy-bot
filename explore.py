import requests

fixtures_url ="https://fantasy.premierleague.com/api/fixtures/"
fixtures_response = requests.get(fixtures_url)
fixtures_data=fixtures_response.json()
print(fixtures_response.status_code)
print(type(fixtures_data))
#print(data[0])

upcoming_fixtures=[]
for match in fixtures_data:
    if not match["finished"]:
        upcoming_fixtures.append(match)
#print(len(upcoming_fixtures))

def get_team_fixtures(team_id):
    result=[]
    for match in upcoming_fixtures:
        if team_id==match["team_a"] or team_id==match["team_h"]:
            result.append(match)
    result_sorted=sorted(result,key=lambda match:match["event"],reverse=False)
    return result_sorted
     
fixtures_team_1 = get_team_fixtures(1)
#print(len(fixtures_team_1))
#print(fixtures_team_1[0])
#print(fixtures_team_1)

def get_difficulty_for_team(match, team_id):
    if team_id == match["team_a"]:
        return match["team_a_difficulty"]
    else:
         return match["team_h_difficulty"]

def get_average_difficulty(team_id):
    fixtures_team=get_team_fixtures(team_id)
    difficulty_list=[]
    for difficulty in fixtures_team[0:3]:
        difficulty_list.append(get_difficulty_for_team(difficulty,team_id))
    match=sum(difficulty_list)/len(difficulty_list)
    return match
#p=get_average_difficulty(1)
#print(p)

difficulty_map={}
for id in range(1,21):
    difficulty_map[id]=get_average_difficulty(id)

print(difficulty_map)
