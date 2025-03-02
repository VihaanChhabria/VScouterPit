import csv
import requests
from requests.auth import HTTPBasicAuth
import os


def loadENV(filename: str):
    with open(filename) as f:
        for line in f:
            if line.strip() and not line.startswith(
                "#"
            ):  # Ignore empty lines and comments
                key, value = line.strip().split("=", 1)
                os.environ[key] = value  # Set as environment variable


def openCSV(path: str) -> list[list[str]]:
    with open(path, "r", newline="", encoding="utf-8") as file:
        csvReader = csv.reader(file, delimiter=";", quotechar='"')
        formattedCSV: list[list[str]] = []
        for row in csvReader:
            formattedCSV.append(row)
        return formattedCSV


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
        with open(f"{teamNum}Robot.jpg", "wb") as file:
            file.write(response.content)


if __name__ == "__main__":
    loadENV(".env")
    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")
    data = openCSV("VScouter_Pit_Scouting.csv")

    picturesURLs = getColumnByHeader(data, "Take a picture of the team’s robot._URL")[
        1:
    ]
    teamNums = getColumnByHeader(data, "What is the team you are pit scouting?")[1:]

    for pictureURL, teamNum in zip(picturesURLs, teamNums):
        getImageFromURL(pictureURL, teamNum)
