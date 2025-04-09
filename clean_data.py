import pandas as pd
import json
import csv

banner_order = [
            'farewell-of-snezhnaya-5', 
            'drifting-luminescence-4', 
            'moment-of-bloom-5', 
            'gentry-of-hermitage-6', 
            'sparkling-steps-4',
            'the-hearths-ashen-shadow-2', 
            'immaculate-pulse-3', 
            'reign-of-serenity-4', 
            'the-heron_s-court-4', 
            'the-transcendent-one-returns-2', 
            'oni_s-royale-4', 
            'chanson-of-many-waters-2', 
            'tempestuous-destiny-1', 
            'azure-excursion-3', 
            'decree-of-the-deeps-3', 
            'leaves-in-the-wind-5'
]



# with open('example.csv', 'w') as file:
#     csv_writer = csv.writer(file)
#     csv_writer.writerow(["ID", "IGN", "Group", "Category", "Pulls Saved", 
#                         "Banner Name", "Character Name", "Class", "Tier", "Gender",
#                         "Action", "Status",
#                         "Reward State", "G'",
#                         "Pity", "Pulls Spent", "Pity 5-Star", "Total Pulls Spent", "Win Pulls", "Total Win Pulls",
#                         "Boss"])

def sort_banners(data):
    if not isinstance(data, dict):
        return data
    sorted_data = data.get('histories', {}) 
    data["histories"] = {
        k: sorted_data[k] 
        for k in banner_order 
        if k in sorted_data
    }
    return data

data = pd.read_csv('data.csv', engine="python")
#print(data)

# Parse and Sort JSON data 
data['banner_data'] = data['banner_data'].apply(lambda x: json.loads(x) if pd.notna(x) else None)
parse_data = data['banner_data'].iloc[0]

data['banner_data'] = list(map(sort_banners, data['banner_data']))
#print(json.dumps(data['banner_data'].iloc[0], indent=4))

for entry in data['banner_data']:
    print(entry)
    print("\n")







