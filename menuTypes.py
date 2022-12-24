from enum import Enum

class MenuTypes(Enum):
    BREAKFAST = ("Breakfast Menu")
    LUNCH = ("Lunch Menu", "Main Line")
    SNACK = ("Snack Menu")

def findMenu(input:str) -> MenuTypes:
    for menu in MenuTypes:
        if input.lower().find(menu.name.lower()) != -1:
            return menu

    raise ValueError("Can't find a menu with that name")