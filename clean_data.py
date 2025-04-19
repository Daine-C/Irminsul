import pandas as pd
import json
import math
import csv
import banner_info as bi


ban_info = bi.banner_order

def sort_banners(data):
    if not isinstance(data, dict):
        return data
    sorted_data = data.get('histories', {}) 
    data["histories"] = {
        k: sorted_data[k] 
        for k in ban_info.keys() 
        if k in sorted_data
    }
    return data


data = pd.read_csv('data.csv', engine="python", index_col=0)


# Parse and Sort JSON data 
data['banner_data'] = data['banner_data'].apply(lambda x: json.loads(x) if pd.notna(x) else None)
parse_data = data['banner_data'].iloc[0]

data['banner_data'] = list(map(sort_banners, data['banner_data']))
# print(json.dumps(data['banner_data'].iloc[0], indent=4))


def getPulls(startBalance):
    pulls = startBalance['fates']
    if startBalance['primos'] != 0:
        pulls += math.floor(startBalance['primos'] / 160)
    return pulls

def getStatus(item):
    return 1 if item['category'] == 'limited' else 0

def getCarryState(reward_state, previous=None):
    match reward_state:
        case "lose":
            return "guaranteed"
        case "guaranteed" | "win":
            return "50/50"
        case "N/A":
            return previous[13] if previous else "50/50"
        case _:
            return "50/50"

def getTotPullSpent(extraPity, pulls):
    total_pulls = extraPity + pulls
    return total_pulls
    
def getCW(state, pulls):
    print(state, data_list[-1][6], data_list[-1][1])
    if state == 'lose':
        lose_pulls[0] = pulls
        return 'N/A'
    
    if pulls == 0 and state == 'win': return data_list[-1][18]
    elif state == 'guaranteed':
        return lose_pulls[0] + pulls
    elif state == 'win':
        return pulls
    

def getCTW(state, total_pulls, pulls_spent):
    if state == 'lose':
        lose_pulls[1] = total_pulls
        return 'N/A'
    
    if pulls_spent == 0 and state == 'win': 
        total = int(data_list[-1][19]) + total_pulls
        data_list[-1][19] = total
        print(data_list[-1][6], data_list[-1][19])
        return total
    elif state == 'guaranteed':
        return lose_pulls[1] + total_pulls
    elif state == 'win':
        return total_pulls


data_list = []
lose_pulls = [0, 0] # [Cw, CTw]
def cleanData():
    for id in data.index.tolist():
        if id:
            histories = data.loc[id, 'banner_data']['histories']
            for banner, details in histories.items():
                expenses = details['expenses']
                action = details['action']
                boss = details['defeat']
                pullBanner = expenses['pullsSpent']
                banner_meta = ban_info[banner]

                items = details.get('item', [])
                if not items:
                    data_list.append([id, data.loc[id, 'ign'], 'group', data.loc[id, 'group'], getPulls(expenses['startBalance']),
                                    banner, *banner_meta, 
                                    action, 0, 
                                    'N/A', getCarryState('N/A', data_list[-1] if data_list else None),
                                    'N/A', #data_list[-1][15] if data_list else 0, # ask if Pity' from previous entry should be considered
                                    pullBanner, 'N/A', 'N/A', # pulls spent, P(5*), C(T)
                                    'N/A', 
                                    'N/A', 
                                    boss # ask if per item ba ibutang ang value sa boss. 
                                    ])
                else:                    
                    data_list.extend([id, data.loc[id, 'ign'], 'group', data.loc[id, 'group'], getPulls(expenses['startBalance']), 
                                        banner, *banner_meta,
                                        action, getStatus(item), 
                                        item['status'], getCarryState(item['status'], data_list[-1]),
                                        item['extraPity'], item['totalPulls'], item['pity'], # P', C, P(5*)
                                        getTotPullSpent(item['extraPity'], item['totalPulls']), 
                                        getCW(item['status'], item['totalPulls']),
                                        getCTW(item['status'], getTotPullSpent(item['extraPity'], item['totalPulls']), item['totalPulls']),
                                        boss ] for item in items
                                        )
                
column_list = ["ID", "IGN", "Group", "Category", "Pulls Saved", 
                        "Banner Name", "Character Name", "Class", "Tier", "Gender",
                        "Action", "Status",
                        "Reward State", "G'",
                        "Pity", "Pulls Spent", "Pity 5-Star", "Total Pulls Spent", "Win Pulls", "Total Win Pulls",
                        "Boss"]
cleanData()
print(column_list)
print(*data_list, sep="\n")

with open('example.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["ID", "IGN", "Group", "Category", "Pulls Saved", 
                        "Banner Name", "Character Name", "Class", "Tier", "Gender",
                        "Action", "Status",
                        "Reward State", "G'",
                        "Pity", "Pulls Spent", "Pity 5-Star", "Total Pulls Spent", "Win Pulls", "Total Win Pulls",
                        "Boss"])
    for row in data_list:
        csv_writer.writerow(row)
# data_dict = {
#     "ID": data.index.tolist(),
#     "IGN": data['ign'].tolist(),
#     "Group": [],
#     "Category": data['group'].tolist()
# }
    
# print(data_dict)






