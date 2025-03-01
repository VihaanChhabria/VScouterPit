import csv


def openCSV(path: str) -> list[list[str]]:
    with open(path, "r", newline="", encoding="utf-8") as file:
        csvReader = csv.reader(file)
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


if __name__ == "__main__":
    openCSV("parsing/VScouter_Pit_Scouting.csv")
