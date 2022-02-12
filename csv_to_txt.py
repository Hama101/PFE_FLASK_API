import pandas as pd


data = pd.DataFrame(pd.read_csv("label.csv"))

#loop through data["name"] and save it to a label.txt file
for i in data["name"]:
    with open("label.txt", "w") as f:
        print(i)
        f.write(i + "\n")

