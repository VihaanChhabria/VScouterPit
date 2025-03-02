import csv
import os


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


def deleteColumnByHeader(csvFile: list[list[str]], headerName: str) -> list[list[str]]:
    columnIndex = -1
    for headerIndex, header in enumerate(csvFile[0]):
        if header == headerName:
            columnIndex = headerIndex
            break

    if columnIndex == -1:
        return csvFile

    for row in csvFile:
        del row[columnIndex]

    return csvFile


def addColumn(currentData: list[list[str]], newColumn: list[str]):
    for rowIndex, row in enumerate(currentData):
        row.append(newColumn[rowIndex])
    return currentData
