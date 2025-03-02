import csv
import requests
from requests.auth import HTTPBasicAuth
import os


def loadENV(filename: str):
    with open(filename) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


def envCheck():
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


def openCSV(path: str) -> list[list[str]]:
    with open(path, "r", newline="", encoding="utf-8") as file:
        csvReader = csv.reader(file, delimiter=";", quotechar='"')
        formattedCSV: list[list[str]] = []
        for row in csvReader:
            formattedCSV.append(row)
        return formattedCSV


def getAllData() -> list[list[str]]:
    fullPitData: list[list[str]] = []
    for pitDataFileNameIndex, pitDataFileName in enumerate(
        os.listdir("data/pit_data/")
    ):
        if pitDataFileNameIndex == 0:
            fullPitData += openCSV("data/pit_data/" + pitDataFileName)
        else:
            fullPitData += openCSV("data/pit_data/" + pitDataFileName)[1:]
    return fullPitData


def getRow(csvFile: list[list[str]], rowNum: int) -> list[str]:
    for rowIndex, row in enumerate(csvFile):
        if rowIndex == rowNum:
            return row
    return []


def getColumnByIndex(csvFile: list[list[str]], columnNum: int) -> list[str]:
    column: list[str] = []
    for row in csvFile:
        for cellIndex, cell in enumerate(row):
            if cellIndex == columnNum:
                column.append(cell)
    return column


def getColumnByHeader(csvFile: list[list[str]], headerName: str) -> list[str]:
    columnIndex: int = 0
    for headerIndex, header in enumerate(csvFile[0]):
        if header == headerName:
            columnIndex = headerIndex

    return getColumnByIndex(csvFile, columnIndex)


def addColumn(currentData: list[list[str]], newColumn: list[str]):
    for rowIndex, row in enumerate(currentData):
        row.append(newColumn[rowIndex])
    return currentData


def getImageFromURL(url: str, teamNum: str):
    if USERNAME and PASSWORD:

        response: requests.Response = requests.get(
            url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
        )
        with open(f"data/robot_images/{teamNum}Robot.jpg", "wb") as file:
            file.write(response.content)


if __name__ == "__main__":
    getAllData()

    envCheck()
    loadENV(".env")

    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")

    data = getAllData()

    picturesURLs = getColumnByHeader(data, "Take a picture of the team’s robot._URL")[
        1:
    ]
    teamNums = getColumnByHeader(data, "What is the team you are pit scouting?")[1:]

    for pictureURL, teamNum in zip(picturesURLs, teamNums):
        getImageFromURL(pictureURL, teamNum)
