import json, os

class School:
    def __init__(self, schoolName: str):
        schoolName = str(schoolName).strip().title()
        f = open(os.path.join(os.path.dirname(__file__), "schools.json"))
        table = json.load(f)
        name = None
        code1 = None
        code2 = None
        imageURL = None 
        for term in table["schools"]:
            # if term["name"].find(schoolName) != -1 or (term["name"] + " School").find(schoolName) != -1 or term["name"].find(schoolName.split(" ")[0]) != -1: #really only the last statement is needed since it'll be true if the others are, but keeping them here for now
            if term["name"].find(schoolName.split(" ")[0]) != -1: #if other schools that have Provo in the name are added, this should be changed
                name = term["name"]
                code1 = term["siteCode1"]
                code2 = term["siteCode2"]
                imageURL = term["iconURL"]
        f.close()
        if code1 == None:
            raise ValueError("Can't find the specified school")
        else:
            self.name = name
            self.code1 = code1
            self.code2 = code2
            self.imageURL = imageURL