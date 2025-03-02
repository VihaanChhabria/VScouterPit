import requests
from requests.auth import HTTPBasicAuth
import os
import csv_utils


def loadENV(filename: str):
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            for key, value in {
                "USERNAME": "your_username_here",
                "PASSWORD": "your_password_here",
            }.items():
                f.write(f"{key}={value}\n")
        print(
            "Created a .env file as it was not detected. Please update it with your credentials."
        )
        exit()

    with open(filename) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


def getImageFromURL(url: str, teamNum: str):
    if USERNAME and PASSWORD:

        response: requests.Response = requests.get(
            url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
        )
        with open(f"data/robot_images/{teamNum}Robot.jpg", "wb") as file:
            file.write(response.content)


if __name__ == "__main__":
    loadENV(".env")

    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")

    data = csv_utils.getAllData()

    picturesURLs = csv_utils.getColumnByHeader(
        data, "Take a picture of the team’s robot._URL"
    )[1:]
    teamNums = csv_utils.getColumnByHeader(
        data, "What is the team you are pit scouting?"
    )[1:]

    for pictureURL, teamNum in zip(picturesURLs, teamNums):
        getImageFromURL(pictureURL, teamNum)
