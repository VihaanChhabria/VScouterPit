import pandas as pd
import os
import keyboard
import mouse
import time
import pyautogui

data_dir = "../parsing/data/output_data/"

csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

if not csv_files:
    print("No CSV files found in the output_data directory.")
    exit()

print("Available data files:")
for idx, file in enumerate(csv_files, 1):
    print(f"{idx}. {file}")

while True:
    try:
        choice = int(input("Enter the number of the file you want to load: ")) - 1
        if 0 <= choice < len(csv_files):
            selected_file = csv_files[choice]
            break
        else:
            print("Invalid selection. Please enter a valid number.")
    except:
        print("Invalid input. Please enter a number.")

df = pd.read_csv(os.path.join(data_dir, selected_file))  # type: ignore
print(f"Loaded: {selected_file}")

teams = df["What is the team you are pit scouting?"].astype(str)

time.sleep(3)

for team in teams:
    keyboard.write(team)
    time.sleep(0.5)
    mouse.click()
    time.sleep(0.5)
    image = pyautogui.screenshot()
    image.save(os.path.join("./teamdata/", f"{team}.png"))
    print(f"Screenshot saved for team {team}")
    time.sleep(0.15)
    keyboard.write("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")