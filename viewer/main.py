import pandas as pd
import tkinter as tk
from tkinter import Label, Entry, Button
from PIL import Image, ImageTk  # type: ignore
import os

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
        return

    row = filtered_df.iloc[0]  # type: ignore

    name_label.config(text=f"Name: {row['What is your name?']}")
    team_label.config(text=f"Team: {row['What is the team you are pit scouting?']}")
    vibe_label.config(text=f"Vibe Rating: {row['vibe rating']}")

    try:
        img = Image.open(row["robot images"])  # type: ignore

        # Get current image size
        img_width, img_height = img.size  # type: ignore
        max_height = 460

        # Calculate the aspect ratio
        aspect_ratio: float = img_width / img_height  # type: ignore

        new_height = max_height
        new_width = int(new_height * aspect_ratio)  # type: ignore

        img = img.resize((new_width, new_height), Image.ANTIALIAS)  # type: ignore
        img = ImageTk.PhotoImage(img)  # type: ignore

        image_label.config(image=img)
        image_label.image = img  # type: ignore
    except Exception as e:
        image_label.config(text=f"Error loading image: {e}")


root = tk.Tk()
root.title("FRC Scouting Data Viewer")
root.geometry("800x600")
root.resizable(False, False)

team_entry = Entry(root, font=("Arial", 14))
team_entry.pack()

search_button = Button(root, text="Search", command=lambda: display_data(team_entry.get()))  # type: ignore
search_button.pack()

name_label = Label(root, text="", font=("Arial", 14))
name_label.pack()

team_label = Label(root, text="", font=("Arial", 14))
team_label.pack()

vibe_label = Label(root, text="", font=("Arial", 14))
vibe_label.pack()

image_label = Label(root)
image_label.pack()

root.mainloop()
