import pandas as pd
import json
import math
import csv
import banner_info as bi

# with open('example.csv', 'w') as file:
#     csv_writer = csv.writer(file)
#     csv_writer.writerow(["ID", "IGN", "Group", "Category", "Pulls Saved", 
#                         "Banner Name", "Character Name", "Class", "Tier", "Gender",
#                         "Action", "Status",
#                         "Reward State", "G'",
#                         "Pity", "Pulls Spent", "Pity 5-Star", "Total Pulls Spent", "Win Pulls", "Total Win Pulls",
#                         "Boss"])

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
            return previous[-1] if previous else "50/50"
        case _:
            return "50/50"

    

data_list = []
def cleanData():
    for id in data.index.tolist():
        if id:
            histories = data.loc[id, 'banner_data']['histories']
            for banner, details in histories.items():
                expenses = details['expenses']
                action = details['action']
                banner_meta = ban_info[banner]

                items = details.get('item', [])
                if not items:
                    data_list.append([id, data.loc[id, 'ign'], 'group', data.loc[id, 'group'], getPulls(expenses['startBalance']),
                                    banner, *banner_meta, 
                                    action, 0, 
                                    'N/A', getCarryState('N/A', data_list[-1] if data_list else None) ])
                else:                    
                    data_list.extend([id, data.loc[id, 'ign'], 'group', data.loc[id, 'group'], getPulls(expenses['startBalance']), 
                                        banner, *banner_meta,
                                        action, getStatus(item), 
                                        item['status'], getCarryState(item['status'], data_list[-1])] for item in items
                                        )
                

cleanData()
print(*data_list, sep="\n")
# data_dict = {
#     "ID": data.index.tolist(),
#     "IGN": data['ign'].tolist(),
#     "Group": [],
#     "Category": data['group'].tolist()
# }
    
# print(data_dict)






