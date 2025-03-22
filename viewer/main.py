import pandas as pd
import tkinter as tk
from tkinter import Label, Entry, Button
from PIL import Image, ImageTk  # type: ignore
import os


def bitStringToBoolString(s: str) -> str:
    return str(bool(int(s)))


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


def display_data(team_number: int):
    filtered_df = df[
        df["What is the team you are pit scouting?"].astype(str) == str(team_number)
    ]
    if filtered_df.empty:
        name_label.config(text="No data found for this team")
        team_label.config(text="")
        vibe_label.config(text="")
        image_label.config(image="", text="No Image")
        drive_label.config(text="")
        weight_label.config(text="")
        l1coral_label.config(text="")
        l2coral_label.config(text="")
        l3coral_label.config(text="")
        l4coral_label.config(text="")
        coralground_label.config(text="")
        coralstation_label.config(text="")
        algaereef_label.config(text="")
        algaeground_label.config(text="")
        algaeprocessor_label.config(text="")
        algaenet_label.config(text="")
        autovariantion_label.config(text="")
        return

    row = filtered_df.iloc[0]  # type: ignore

    name_label.config(text=f"Name: {row['What is your name?']}")
    team_label.config(text=f"Team: {row['What is the team you are pit scouting?']}")
    vibe_label.config(text=f"Vibe Rating: {row['vibe rating']}")
    drive_label.config(text=f"Robot Drive: {row['What\'s the robots drivetrain?']}")
    weight_label.config(text=f'Robot Weight: {row["What is the robots weight?"]}')
    l1coral_label.config(
        text=f'L1 Coral?: {bitStringToBoolString(row["What are their robots scoring abilities?/L1 Coral Place"])}'
    )
    l2coral_label.config(
        text=f'L2 Coral?: {bitStringToBoolString(row["What are their robots scoring abilities?/L2 Coral Place"])}'
    )
    l3coral_label.config(
        text=f'L3 Coral?: {bitStringToBoolString(row["What are their robots scoring abilities?/L3 Coral Place"])}'
    )
    l4coral_label.config(
        text=f'L4 Coral?: {bitStringToBoolString(row["What are their robots scoring abilities?/L4 Coral Place"])}'
    )
    coralground_label.config(
        text=f'Coral Ground Pick: {bitStringToBoolString(row["What are their robots scoring abilities?/Coral Ground Pick"])}'
    )
    coralstation_label.config(
        text=f'Coral Station Pick?: {bitStringToBoolString(row["What are their robots scoring abilities?/Coral Station Pick"])}'
    )
    algaereef_label.config(
        text=f'Algae Reef Removal?: {bitStringToBoolString(row["What are their robots scoring abilities?/Algae Reef Removal"])}'
    )
    algaeground_label.config(
        text=f'Algae Ground Pick?: {bitStringToBoolString(row["What are their robots scoring abilities?/Algae Ground Pick"])}'
    )
    algaeprocessor_label.config(
        text=f'Algae Processor?: {bitStringToBoolString(row["What are their robots scoring abilities?/Algae Processor Place"])}'
    )
    algaenet_label.config(
        text=f'Algae Net Shot?: {bitStringToBoolString(row["What are their robots scoring abilities?/Algae Net Shot Place"])}'
    )
    autovariantion_label.config(
        text=f'Auton Variations: {row["How many auton variations do they have?"]}'
    )

    try:
        img = Image.open(row["robot images"])  # type: ignore

        # Get current image size
        img_width, img_height = img.size  # type: ignore
        max_height = 460

        # Calculate the aspect ratio
        aspect_ratio: float = img_width / img_height  # type: ignore

        new_height = max_height
        new_width = int(new_height * aspect_ratio)  # type: ignore

        img = img.resize((new_width, new_height))  # type: ignore
        img = ImageTk.PhotoImage(img)  # type: ignore

        image_label.config(image=img)
        image_label.image = img  # type: ignore
    except Exception as e:
        image_label.config(text=f"Error loading image: {e}")


root = tk.Tk()
root.title("VScouter Pit Data Viewer")
root.geometry("1000x600")
root.resizable(False, False)

team_entry = Entry(root, font=("Arial", 14))
team_entry.pack()

search_button = Button(root, text="Search", command=lambda: display_data(team_entry.get()))  # type: ignore
search_button.pack()

frame = tk.Frame(root)
frame.pack()

robot_details = tk.Frame(frame)
robot_details.grid(column=0, row=1)

name_label = Label(robot_details, text="", font=("Arial", 14))
name_label.pack()

team_label = Label(robot_details, text="", font=("Arial", 14))
team_label.pack()

vibe_label = Label(robot_details, text="", font=("Arial", 14))
vibe_label.pack()

drive_label = Label(robot_details, text="", font=("Arial", 14))
drive_label.pack()

weight_label = Label(robot_details, text="", font=("Arial", 14))
weight_label.pack()

l1coral_label = Label(robot_details, text="", font=("Arial", 14))
l1coral_label.pack()

l2coral_label = Label(robot_details, text="", font=("Arial", 14))
l2coral_label.pack()

l3coral_label = Label(robot_details, text="", font=("Arial", 14))
l3coral_label.pack()

l4coral_label = Label(robot_details, text="", font=("Arial", 14))
l4coral_label.pack()

coralground_label = Label(robot_details, text="", font=("Arial", 14))
coralground_label.pack()

coralstation_label = Label(robot_details, text="", font=("Arial", 14))
coralstation_label.pack()

algaereef_label = Label(robot_details, text="", font=("Arial", 14))
algaereef_label.pack()

algaeground_label = Label(robot_details, text="", font=("Arial", 14))
algaeground_label.pack()

algaeprocessor_label = Label(robot_details, text="", font=("Arial", 14))
algaeprocessor_label.pack()

algaenet_label = Label(robot_details, text="", font=("Arial", 14))
algaenet_label.pack()

autovariantion_label = Label(robot_details, text="", font=("Arial", 14))
autovariantion_label.pack()

image_label = Label(frame)
image_label.grid(column=1, row=1)

root.mainloop()
