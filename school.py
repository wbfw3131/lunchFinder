import json, os
from enum import Enum

class School:
    def __init__(self, schoolName: str):
        schoolName = str(schoolName).strip().title()
        f = open(os.path.join(os.path.dirname(__file__), "schools.json"))
        table = json.load(f)
        f.close()
        # for district in table.values():
        # for district in table.items():
        for district in table.keys():
            for term in table[district]:
                # if term["name"].find(schoolName) != -1 or (term["name"] + " School").find(schoolName) != -1 or term["name"].find(schoolName.split(" ")[0]) != -1: #really only the last statement is needed since it'll be true if the others are, but keeping them here for now
                if term["name"].find(schoolName.split(" ")[0]) != -1: #if other schools that have Provo in the name are added, this should be changed
                    for attribute in term:
                        self.__setattr__(attribute, term[attribute])
                    self.__setattr__("district", district)
                    
                    
                    # name = term["name"]
                    # code1 = term["siteCode1"]
                    # code2 = term["siteCode2"]
                    # imageURL = term["iconURL"]
                    return
        

        raise ValueError("Can't find the specified school")


        
#TODO figure out if I want to use an enum or just normal strings
class District(Enum):
    PROVO = "Provo"
    ALPINE = "Alpine"