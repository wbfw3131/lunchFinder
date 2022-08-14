import requests
import datetime
from school import School



# def parseItems(menu):
#     for item in menu["items"]:
#         print(item["product"]["name"])

        
def dayLunch(day: str = "today", schoolStr: str or School = School("Provo High")) -> str:
    """Takes in a date string in MM/DD/YYYY format (or "today")

    Returns a string concatenated with all the items for lunch (except milks)"""
    if type(schoolStr) == str:
        schoolQueried = School(schoolStr)
    else:
        schoolQueried = schoolStr

    if day.lower() == "today":
        date = datetime.date.today()
        #print(date)
    else:
        date = datetime.datetime.strptime(day, '%m/%d/%Y').date()

    if datetime.date.weekday(date) == 5 or datetime.date.weekday(date) == 6:
        return "That day isn't a weekday, so there's no school"
    # elif date.month >= (datetime.date.today().month + 1): # and datetime.date().today().day() < 20:
    #     return "I don't think the lunch for that month is posted yet"

    content = makeRequest(schoolQueried, date)

    food = makeList(content)

    #TODO
    #Make sure logic is sound
    if food == []: #figuring out why an empty response was returned
        if date.month >= (datetime.date.today().month + 1): #if the date is next month from today
            weekLater = date + datetime.timedelta(weeks=1)
            weekEarlier = date + datetime.timedelta(weeks=-1)
            if makeList(makeRequest(schoolQueried, weekLater)) != []: #if there's anything for lunch a week after the selected date
                return "There's no school on that day" 
            else:
                if weekEarlier.month == date.month:
                    if makeList(makeRequest(schoolQueried, weekEarlier)) != []: #if there's anything for lunch a week before the date
                        return "There's no school on that day"
                    else:
                        return "I don't think the lunch for that month is posted yet"
                else:
                    return "I don't think the lunch for that date is available anymore"
        else:
            return "I don't think there's school on that day"

    return makeLunch(food, date)


def makeLunch(foodList: list, date: datetime.date) -> str:
    """Puts together all items from a list into a string"""
    terms = []
    first = True
    finalString = ""
    for food in foodList:
        if first:
            if date == datetime.date.today():
                finalString = f"Today's lunch is **{food}** with "
            elif date == datetime.date.today() + datetime.timedelta(days=1):
                finalString = f"Tomorrow's lunch will be **{food}** with "
            elif date == datetime.date.today() - datetime.timedelta(days=1):
                finalString = f"Yesterday's lunch was **{food}** with "
            else:
                # TODO
                # add dynamic days of the week for current week

                # TODO
                # use datetime.datetime.now().timestamp() to format dates for Discord; ex: <t:1659125077>
                # help here: https://hammertime.cyou

                if date > datetime.date.today():
                    finalString = f"The lunch on {date.strftime('%B')} {date.day}{findNumSuffix(date.day)} will be **{food}** with "
                else:
                    finalString = f"The lunch on {date.strftime('%B')} {date.day}{findNumSuffix(date.day)} was **{food}** with "
            first = False
        else:
            if (food.find("Milk") == -1):
                terms.append(f"{food}")
    # lastTerm = str(terms.pop(len(terms) - 1))
    terms[len(terms)-1] = "and " + terms[len(terms)-1]
    joined = ", ".join(terms)
    finalString = finalString + joined + "."
    return(finalString)

#def makeRequest(siteCode1: int, siteCode2: int, date: datetime.datetime) -> dict:
def makeRequest(schoolQueried: School, date: datetime.date) -> dict:
    """Makes an api request with the site codes and date provided.
    
    Site codes can be found in the url of the lunch menu you want or from the corresponding school in `schools.json`"""
    endpoint = "https://api.isitesoftware.com/graphql"
    headers = {
        'authority': 'api.isitesoftware.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '*/*',
        'origin': 'https://schoolnutritionandfitness.com',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://schoolnutritionandfitness.com/',
        'accept-language': 'en-US,en;q=0.9',
    }
    data = {
    'query': '\nquery mobileSchoolPage($date: String!, $site_code: String!, $site_code2: String!, $useDepth2: Boolean!) {\n  menuTypes(publish_location: "mobile", site:{\n      depth_0_id: $site_code,\n      depth_1_id: $site_code2\n  }) {\n    id\n    name\n    formats\n    items(start_date: $date, end_date: $date) {\n      date,\n      product {\n          id\nname\nallergen_dairy\nallergen_egg\nallergen_fish\nallergen_gluten\nallergen_milk\nallergen_peanut\nallergen_pork\nallergen_shellfish\nallergen_soy\nallergen_treenuts\nallergen_vegetarian\nallergen_wheat\nallergen_other\ncustomAllergens\nimage_url1\nimage_url2\npdf_url\nportion_size\nportion_size_unit\nprice\nprod_allergens\nprod_calcium\nprod_calories\nprod_carbs\nprod_cholesterol\nprod_dietary_fiber\nprod_gram_weight\nprod_iron\nprod_mfg\nprod_protein\nprod_sat_fat\nprod_sodium\nprod_total_fat\nprod_trans_fat\nprod_vita_iu\nprod_vita_re\nprod_vitc\nsugar\nis_ancillary\nmealsPlusCustomAllergens\nmealsPlusCustomAttributes\n\n          long_description\n          hide_on_mobile\n      }\n    }\n  }\n  listMenus(publish_location:"mobile", site:{\n      depth_0_id: $site_code,\n      depth_1_id: $site_code2\n  }) {\n    id\n    name\n    items{\n      product {\n        id\nname\nallergen_dairy\nallergen_egg\nallergen_fish\nallergen_gluten\nallergen_milk\nallergen_peanut\nallergen_pork\nallergen_shellfish\nallergen_soy\nallergen_treenuts\nallergen_vegetarian\nallergen_wheat\nallergen_other\ncustomAllergens\nimage_url1\nimage_url2\npdf_url\nportion_size\nportion_size_unit\nprice\nprod_allergens\nprod_calcium\nprod_calories\nprod_carbs\nprod_cholesterol\nprod_dietary_fiber\nprod_gram_weight\nprod_iron\nprod_mfg\nprod_protein\nprod_sat_fat\nprod_sodium\nprod_total_fat\nprod_trans_fat\nprod_vita_iu\nprod_vita_re\nprod_vitc\nsugar\nis_ancillary\nmealsPlusCustomAllergens\nmealsPlusCustomAttributes\n\n        long_description\n        hide_on_mobile\n      }\n    }\n  }\n  pdfMenus(site:{\n      depth_0_id: $site_code\n  }) {\n    id\n    name\n    url\n  }\n  site (depth: 0, id: $site_code) @skip(if: $useDepth2) {\n    id,\n    parent_id,\n    name,\n    logo_url\n    organization {\n  id,\n  name,\n  logo_url\n  OnlineMenuDesignSettings {\n    customAllergens {\n        field\n        img\n        label\n        tooltip\n    }\n    mealsPlusCustomAllergens {\n      field\n      img\n      label\n      tooltip\n      mealsPlusId\n    }\n    mealsPlusCustomAttributes {\n      field\n      img\n      label\n      tooltip\n      mealsPlusId\n    }\n    disableAllergen\n    showAllergens\n    allergenFilterEnabled\n    ratingEmojiShow\n  }\n  SnafDistrict {\n    url_online_pay\n  }\n  SnafSettings {\n    enable_surveys\n    enable_announcements\n  }\n  OnlineOrderingSettings {\n    enableSlc\n    enableTlc\n  }\n  apps {\n    onlineordering {\n      enable_linq\n    }\n  }\n}\n  }\n  site2: site (depth: 1, id: $site_code2) @include(if: $useDepth2) {\n    id,\n    parent_id,\n    name,\n    logo_url,\n    organization {\n  id,\n  name,\n  logo_url\n  OnlineMenuDesignSettings {\n    customAllergens {\n        field\n        img\n        label\n        tooltip\n    }\n    mealsPlusCustomAllergens {\n      field\n      img\n      label\n      tooltip\n      mealsPlusId\n    }\n    mealsPlusCustomAttributes {\n      field\n      img\n      label\n      tooltip\n      mealsPlusId\n    }\n    disableAllergen\n    showAllergens\n    allergenFilterEnabled\n    ratingEmojiShow\n  }\n  SnafDistrict {\n    url_online_pay\n  }\n  SnafSettings {\n    enable_surveys\n    enable_announcements\n  }\n  OnlineOrderingSettings {\n    enableSlc\n    enableTlc\n  }\n  apps {\n    onlineordering {\n      enable_linq\n    }\n  }\n}\n  }\n}\n',
    'variables': '{"date":"%s","site_code":"%i","site_code2":"%i","useDepth2":true}' % (date.strftime('%m/%d/%Y'), schoolQueried.code1, schoolQueried.code2)}
    response = requests.post(endpoint, headers=headers, data=data)
    rawContent = response.json()
    return rawContent

def makeList(rawContent: dict) -> list:
    "Takes in the raw dictionary from an API request and puts all the items in a list"
    for menu in rawContent["data"]["menuTypes"]:

        menuName = menu["name"]
        if menuName in ("Lunch Menu", "Main Line"):
            food = []
            for item in menu["items"]:
                food.append(item["product"]["name"].strip())
            return food

def findNumSuffix(num: int) -> str:
    """Finds the suffix of a number and returns it
    
    Ex: 1 returns 'st', 3 returns 'rd'"""

    #corr. #s:  0     1     2     3     4     5     6     7     8     9
    suffixes = ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")
    num %= 100
    if num > 10 and num < 14:
        return "th"
    else:
        return suffixes[num%10]

if __name__ == "__main__":
    # print(dayLunch(day = "5/2/2022", schoolStr="Timpview"))
    # print(dayLunch("8/16/2022"))
    print(dayLunch())