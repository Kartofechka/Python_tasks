from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service())
driver.get("https://sudoku.us.com/")


def is_valid(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
        box_row = 3 * (row // 3) + i // 3
        box_col = 3 * (col // 3) + i % 3
        if grid[box_row][box_col] == num:
            return False
    return True

def solve_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True


grid = []
for y in range(9):
    row = []
    for x in range(9):
        cell = driver.find_element(By.CLASS_NAME, f"cell-{x}-{y}")
        value = cell.get_attribute("value")
        readonly = cell.get_attribute("readonly")
        if value and value.isdigit():
            row.append(int(value))
        else:
            row.append(0)
    grid.append(row)


if solve_sudoku(grid):
    for y in range(9):
        for x in range(9):
            cell = driver.find_element(By.CLASS_NAME, f"cell-{x}-{y}")
            readonly = cell.get_attribute("readonly")
            if not readonly:
                cell.clear()
                cell.send_keys(str(grid[y][x]))
    print("Победа")
else:
    print("Unluck.")

input("Тык что нибудь")