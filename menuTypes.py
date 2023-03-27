from enum import Enum

class MenuTypes(Enum):
    BREAKFAST = ("Breakfast Menu", 1487)
    LUNCH = ("Lunch Menu", "Main Line", 1488)
    SNACK = ("Snack Menu")


    def __init__(self, *_) -> None:
        # not doing this since we can't get edit `self.value` later since it's a tuple
        # tempList:list = [val for val in self.value]

        if type(self.value[-1]) == int:
            self.__setattr__("alpineID", self.value[-1])
        else:
            self.__setattr__("alpineID", None)

        # self.value = (val for val in tempList)
        super().__init__()

def findMenu(input:str) -> MenuTypes:
    for menu in MenuTypes:
        if input.lower().find(menu.name.lower()) != -1:
            return menu

    raise ValueError("Can't find a menu with that name")