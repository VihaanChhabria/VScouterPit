import requests
from requests.auth import HTTPBasicAuth
import os
import csv_utils
from PIL import Image  # type: ignore
import io
import csv
import time


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


def cleanData(data: list[list[str]]) -> list[list[str]]:
    for i, header in enumerate(data[0]):
        if header == "end":
            data[0][i] = "submission time"
        elif header == "Rate it:":
            data[0][i] = "vibe rating"

    data = csv_utils.deleteColumnByHeader(data, "start")
    data = csv_utils.deleteColumnByHeader(data, "What are the vibes of the team?")
    data = csv_utils.deleteColumnByHeader(data, "Take a picture of the team’s robot.")
    data = csv_utils.deleteColumnByHeader(
        data, "Take a picture of the team’s robot._URL"
    )
    data = csv_utils.deleteColumnByHeader(data, "_id")
    data = csv_utils.deleteColumnByHeader(data, "_uuid")
    data = csv_utils.deleteColumnByHeader(data, "_submission_time")
    data = csv_utils.deleteColumnByHeader(data, "_validation_status")
    data = csv_utils.deleteColumnByHeader(data, "_notes")
    data = csv_utils.deleteColumnByHeader(data, "_status")
    data = csv_utils.deleteColumnByHeader(data, "_submitted_by")
    data = csv_utils.deleteColumnByHeader(data, "__version__")
    data = csv_utils.deleteColumnByHeader(data, "_index")
    data = csv_utils.deleteColumnByHeader(data, "_tags")

    return data


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
    robotPicPaths: list[str] = ["robot images"]
    for pictureURL, teamNum in zip(picturesURLs, teamNums):
        if not teamNum in doneTeamNums:
            doneTeamNums.append(teamNum)
            getImageFromURLAndDownload(pictureURL, teamNum)
        else:
            image1 = Image.open(f"data/robot_images/{teamNum}Robot.jpg")  # type: ignore
            image2 = Image.open(io.BytesIO(getImageFromURL(pictureURL)))  # type: ignore
            mergeImages(image1, image2).save(f"data/robot_images/{teamNum}Robot.jpg")  # type: ignore
        robotPicPaths.append(f"{os.getcwd()}\\data\\robot_images\\{teamNum}Robot.jpg")

    data = cleanData(data)
    data = csv_utils.addColumn(data, robotPicPaths)
    
    current_time = time.strftime("%Y%m%d-%H%M%S")
    output_filename = f"data/output_data/VScouter_Pit_Data_Parsed_{current_time}.csv"
    with open(output_filename, mode="w", newline="") as file:
        writer = csv.writer(file)  # Create a CSV writer
        writer.writerows(data)      # Write all rows at once
    

if __name__ == "__main__":
    main()
