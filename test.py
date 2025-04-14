import csv

with open('example.csv', 'w') as file:
    csv_writer = csv.writer(file)
    # csv_writer.writerow(["ID", "IGN", "Group", "Category", "Pulls Saved", 
    #                     "Banner Name", "Character Name", "Class", "Tier", "Gender",
    #                     "Action", "Status",
    #                     "Reward State", "G'",
    #                     "Pity", "Pulls Spent", "Pity 5-Star", "Total Pulls Spent", "Win Pulls", "Total Win Pulls",
    #                     "Boss"])
    csv_writer.writerow()