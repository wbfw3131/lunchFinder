import requests
import datetime
from school import School, District
from message import Message
from menuTypes import MenuTypes, findMenu



# def parseItems(menu):
#     for item in menu["items"]:
#         print(item["product"]["name"])

        
def dayLunch(day: str = "today", schoolStr: str | School = "Provo High", menu: MenuTypes | str = MenuTypes.LUNCH) -> Message:
    """Takes in a date string in MM/DD/YYYY format (or "today" or "tomorrow")

    Returns a string concatenated with all the items for lunch (except milks)"""

    if type(schoolStr) == School:
        schoolQueried = schoolStr
    else:
        schoolQueried = School(schoolStr)

    if day.lower() == "today":
        date = datetime.date.today()
        #print(date)
    elif day.lower() == "tomorrow":
        date = datetime.date.today() + datetime.timedelta(days=1)
    else:
        date = datetime.datetime.strptime(day, '%m/%d/%Y').date()

    #TODO fix this to look in a tuple instead
    if datetime.date.weekday(date) == 5 or datetime.date.weekday(date) == 6:
        return Message(f"{date.strftime('%A')} is a weekend, so there's no school.", False)
    # elif date.month >= (datetime.date.today().month + 1): # and datetime.date().today().day() < 20:
    #     return "I don't think the lunch for that month is posted yet"

    if type(menu) != MenuTypes:
        menu = findMenu(menu)

    content = makeRequest(schoolQueried, date)

    food = makeList(content, schoolQueried, menu)

    #TODO
    #Make sure logic is sound
    #TODO
    #Make error strings have dynamic dates
    if food == []: #figuring out why an empty response was returned
        # TODO this month comparison system breaks with December and January
        # if date.month >= (datetime.date.today().month + 1):        was previously
        if date.month >= (datetime.date.today() + datetime.timedelta(weeks=4)).month: #if the date is next month from today, uses 4 weeks to represent a month
            weekLater = date + datetime.timedelta(weeks=1)
            weekEarlier = date + datetime.timedelta(weeks=-1)
            if makeList(makeRequest(schoolQueried, weekLater), menu) != []: #if there's anything for lunch a week after the selected date
                return Message("There's no school on that day", False)
            else:
                if weekEarlier.month == date.month:
                    if makeList(makeRequest(schoolQueried, weekEarlier), menu) != []: #if there's anything for lunch a week before the date
                        return Message("There's no school on that day", False)
                    else:
                        return Message("I don't think the lunch for that month is posted yet", False)
                else:
                    return Message("I don't think the lunch for that date is available anymore", False)
        else:
            return Message("I don't think there's school on that day", False)

    return makeLunch(food, date, menu)


def makeLunch(foodList: list, date: datetime.date, menu: MenuTypes) -> str:
    """Puts together all food items from a list into a string"""
    preString = ""
    entree = foodList.pop(0)

    if date == datetime.date.today():
        preString = f"Today's {menu.name.lower()} is **{entree}** with "
    elif date == datetime.date.today() + datetime.timedelta(days=1):
        preString = f"Tomorrow's {menu.name.lower()} will be **{entree}** with "
    elif date == datetime.date.today() - datetime.timedelta(days=1):
        preString = f"Yesterday's {menu.name.lower()} was **{entree}** with "
    else:
        if date < datetime.date.today():
            timePreposition = "was"
        else:
            timePreposition = "will be"

        # formula to get date of Monday of the week
        recentMonday = datetime.date.today() - datetime.timedelta(days = datetime.date.today().weekday())

        # strf code reference: https://strftime.org

        if (date - recentMonday) < datetime.timedelta(days=5) and (date - recentMonday) > datetime.timedelta(): #if the date isn't farther than the friday of the this week
            preString = f"The {menu.name.lower()} on {date.strftime('%A')} {timePreposition} **{entree}** with "
        else:
            preString = f"The {menu.name.lower()} on {date.strftime('%B')} {date.day}{findNumSuffix(date.day)} {timePreposition} **{entree}** with "

        # TODO
        # use datetime.datetime.now().timestamp() to format dates for Discord; ex: <t:1659125077>
        # help here: https://hammertime.cyou
        

    foodList[len(foodList)-1] = "and " + foodList[len(foodList)-1]
    joined = ", ".join(foodList)
    finalString = preString + joined + "."
    return(Message(finalString))

#def makeRequest(siteCode1: int, siteCode2: int, date: datetime.datetime) -> dict:
def makeRequest(schoolQueried: School, date: datetime.date) -> dict:
    """Makes an api request with the site codes and date provided.
    
    Site codes can be found in the url of the lunch menu you want or from the corresponding school in `schools.json`"""
    #TODO add switch and case statements

    #Provo returns all menus for a sepcified day, so we filter through the menus in `makelist()`
    if schoolQueried.district == District.PROVO.value:
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
        'variables': '{"date":"%s","site_code":"%i","site_code2":"%i","useDepth2":true}' % (date.strftime('%m/%d/%Y'), schoolQueried.siteCode1, schoolQueried.siteCode2)}
        response = requests.post(endpoint, headers=headers, data=data)
        rawContent = response.json()
        return rawContent
    
    #Alpine returns all of one type of a menu for week, so we find the right date in this method
    elif schoolQueried.district == District.ALPINE.value:
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://alpineschools.nutrislice.com',
            # 'If-None-Match': '"974213cf392f8ec0661abcf82a206545"',
            'Host': 'alpineschools.api.nutrislice.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15',
            'Accept-Language': 'en-US,en;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Connection': 'keep-alive',
            'x-nutrislice-origin': 'alpineschools.nutrislice.com',
            'default_menu_format': 'day'
        }
        response = requests.get(f'https://alpineschools.api.nutrislice.com/menu/api/weeks/school/19505/menu-type/1488/{date.strftime("%Y/%m/%d")}', headers=headers)
        rawContent = response.json()

        for weekday in rawContent["days"]:
            if weekday["date"] == date.strftime("%Y-%m-%d"):
                return weekday

        # return rawContent

def makeList(rawContent: dict, schoolQueried: School, menu: MenuTypes) -> list:
    "Takes in the raw dictionary from an API request and puts all the items in a list"
    food = []

    if schoolQueried.district == District.PROVO.value:
        for menuM in rawContent["data"]["menuTypes"]:
            menuName = menuM["name"]
            if menuName in menu.value:
                for item in menuM["items"]:
                    if (item["product"]["name"].find("Milk") == -1):
                        food.append(item["product"]["name"].strip())
                return food
    
    elif schoolQueried.district == District.ALPINE.value:
        for item in rawContent["menu_items"]:
            if item["food"]:
                food.append(item["food"]["name"].strip())
            else:
                if item["text"] == "Entree options are one Sandwich item and one pizza item from below":
                    food.append("Sandwhiches and Pizza")
                elif item["text"] == "Fruit Options Listed Below":
                    food.append("Fruit")
                # else:
                #     menu.append(item["text"])
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
    # print(dayLunch("1/2/2023", menu="breakfast"))
    print(dayLunch())