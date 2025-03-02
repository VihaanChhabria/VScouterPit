import requests
from requests.auth import HTTPBasicAuth
import os
import csv_utils
from PIL import Image  # type: ignore
import io


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


def getImageFromURLAndDownload(url: str, teamNum: str):
    if USERNAME and PASSWORD:
        response: requests.Response = requests.get(
            url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
        )
        downloadData(f"data/robot_images/{teamNum}Robot.jpg", response.content)


def getImageFromURL(url: str) -> bytes:
    if USERNAME and PASSWORD:
        response: requests.Response = requests.get(
            url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
        )
        return response.content
    return bytes()


def downloadData(path: str, data: bytes):
    with open(path, "wb") as file:
        file.write(data)


def mergeImages(image1, image2):  # type: ignore
    width1, height1 = image1.size  # type: ignore
    width2, height2 = image2.size  # type: ignore

    mergedWidth = width1 + width2  # type: ignore
    mergedHeight = max(height1, height2)  # type: ignore

    mergedImage = Image.new("RGB", (mergedWidth, mergedHeight))  # type: ignore

    mergedImage.paste(image1, (0, 0))  # type: ignore
    mergedImage.paste(image2, (width1, 0))  # type: ignore

    return mergedImage


def main():
    loadENV(".env")

    global USERNAME
    USERNAME = os.environ.get("USERNAME")
    global PASSWORD
    PASSWORD = os.environ.get("PASSWORD")

    data = csv_utils.getAllData()

    picturesURLs = csv_utils.getColumnByHeader(
        data, "Take a picture of the team’s robot._URL"
    )[1:]
    teamNums = csv_utils.getColumnByHeader(
        data, "What is the team you are pit scouting?"
    )[1:]

    doneTeamNums: list[str] = []
    for pictureURL, teamNum in zip(picturesURLs, teamNums):
        if not teamNum in doneTeamNums:
            doneTeamNums.append(teamNum)
            getImageFromURLAndDownload(pictureURL, teamNum)
        else:
            image1 = Image.open(f"data/robot_images/{teamNum}Robot.jpg")  # type: ignore
            image2 = Image.open(io.BytesIO(getImageFromURL(pictureURL)))  # type: ignore
            mergeImages(image1, image2).save(f"data/robot_images/{teamNum}Robot.jpg")  # type: ignore


if __name__ == "__main__":
    main()
