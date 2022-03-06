import requests
import datetime




# print(response.json())


# def parseItems(menu):
#     for item in menu["items"]:
#         print(item["product"]["name"])


        
def dayLunch(day: str = "today", school: str = "Provo High") -> str:
    """Takes in a date string in MM/DD/YYYY format (or "today" or nothing)\n
    Returns a string with concatenated with all the items for lunch"""
    if day == "today":
        date = datetime.date.today()
        #print(date)
    else:
        date = datetime.datetime.strptime(day, '%m/%d/%Y')

    if datetime.date.weekday(date) == 5 or datetime.date.weekday(date) == 6:
        return "There's no school on this day."

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
    school = school.strip()
    if school == "Provo High":
        siteCode = 550
        siteCode2 = 368
    elif school == "Dixon Middle":
        siteCode = 549
        siteCode2 = 366
    data = {
    'query': '\nquery mobileSchoolPage($date: String!, $site_code: String!, $site_code2: String!, $useDepth2: Boolean!) {\n  menuTypes(publish_location: "mobile", site:{\n      depth_0_id: $site_code,\n      depth_1_id: $site_code2\n  }) {\n    id\n    name\n    formats\n    items(start_date: $date, end_date: $date) {\n      date,\n      product {\n          id\nname\nallergen_dairy\nallergen_egg\nallergen_fish\nallergen_gluten\nallergen_milk\nallergen_peanut\nallergen_pork\nallergen_shellfish\nallergen_soy\nallergen_treenuts\nallergen_vegetarian\nallergen_wheat\nallergen_other\ncustomAllergens\nimage_url1\nimage_url2\npdf_url\nportion_size\nportion_size_unit\nprice\nprod_allergens\nprod_calcium\nprod_calories\nprod_carbs\nprod_cholesterol\nprod_dietary_fiber\nprod_gram_weight\nprod_iron\nprod_mfg\nprod_protein\nprod_sat_fat\nprod_sodium\nprod_total_fat\nprod_trans_fat\nprod_vita_iu\nprod_vita_re\nprod_vitc\nsugar\nis_ancillary\nmealsPlusCustomAllergens\nmealsPlusCustomAttributes\n\n          long_description\n          hide_on_mobile\n      }\n    }\n  }\n  listMenus(publish_location:"mobile", site:{\n      depth_0_id: $site_code,\n      depth_1_id: $site_code2\n  }) {\n    id\n    name\n    items{\n      product {\n        id\nname\nallergen_dairy\nallergen_egg\nallergen_fish\nallergen_gluten\nallergen_milk\nallergen_peanut\nallergen_pork\nallergen_shellfish\nallergen_soy\nallergen_treenuts\nallergen_vegetarian\nallergen_wheat\nallergen_other\ncustomAllergens\nimage_url1\nimage_url2\npdf_url\nportion_size\nportion_size_unit\nprice\nprod_allergens\nprod_calcium\nprod_calories\nprod_carbs\nprod_cholesterol\nprod_dietary_fiber\nprod_gram_weight\nprod_iron\nprod_mfg\nprod_protein\nprod_sat_fat\nprod_sodium\nprod_total_fat\nprod_trans_fat\nprod_vita_iu\nprod_vita_re\nprod_vitc\nsugar\nis_ancillary\nmealsPlusCustomAllergens\nmealsPlusCustomAttributes\n\n        long_description\n        hide_on_mobile\n      }\n    }\n  }\n  pdfMenus(site:{\n      depth_0_id: $site_code\n  }) {\n    id\n    name\n    url\n  }\n  site (depth: 0, id: $site_code) @skip(if: $useDepth2) {\n    id,\n    parent_id,\n    name,\n    logo_url\n    organization {\n  id,\n  name,\n  logo_url\n  OnlineMenuDesignSettings {\n    customAllergens {\n        field\n        img\n        label\n        tooltip\n    }\n    mealsPlusCustomAllergens {\n      field\n      img\n      label\n      tooltip\n      mealsPlusId\n    }\n    mealsPlusCustomAttributes {\n      field\n      img\n      label\n      tooltip\n      mealsPlusId\n    }\n    disableAllergen\n    showAllergens\n    allergenFilterEnabled\n    ratingEmojiShow\n  }\n  SnafDistrict {\n    url_online_pay\n  }\n  SnafSettings {\n    enable_surveys\n    enable_announcements\n  }\n  OnlineOrderingSettings {\n    enableSlc\n    enableTlc\n  }\n  apps {\n    onlineordering {\n      enable_linq\n    }\n  }\n}\n  }\n  site2: site (depth: 1, id: $site_code2) @include(if: $useDepth2) {\n    id,\n    parent_id,\n    name,\n    logo_url,\n    organization {\n  id,\n  name,\n  logo_url\n  OnlineMenuDesignSettings {\n    customAllergens {\n        field\n        img\n        label\n        tooltip\n    }\n    mealsPlusCustomAllergens {\n      field\n      img\n      label\n      tooltip\n      mealsPlusId\n    }\n    mealsPlusCustomAttributes {\n      field\n      img\n      label\n      tooltip\n      mealsPlusId\n    }\n    disableAllergen\n    showAllergens\n    allergenFilterEnabled\n    ratingEmojiShow\n  }\n  SnafDistrict {\n    url_online_pay\n  }\n  SnafSettings {\n    enable_surveys\n    enable_announcements\n  }\n  OnlineOrderingSettings {\n    enableSlc\n    enableTlc\n  }\n  apps {\n    onlineordering {\n      enable_linq\n    }\n  }\n}\n  }\n}\n',
    'variables': '{"date":"%s","site_code":"%i","site_code2":"%i","useDepth2":true}' % (date.strftime('%m/%d/%Y'), siteCode, siteCode2)}
    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()
    for menu in content["data"]["menuTypes"]:
        menuName = menu["name"]
        if menuName == "Lunch Menu" or menuName == "Main Line":
            food = []
            for item in menu["items"]:
                food.append(item["product"]["name"].strip())
            # makeLunch(food)
            return makeLunch(food)


def makeLunch(foodList: list) -> str:
    """Puts together all items from a list in a string"""
    terms = []
    first = True
    finalString = ""
    for food in foodList:
        if first:
            finalString = (f"Today for lunch is **{food}** with ")
            first = False
        else:
            if (food.find("Milk") == -1):
                terms.append(f"{food}")
    lastTerm = str(terms.pop(len(terms) - 1))
    joiner = ", "
    joined = joiner.join(terms)
    finalString = finalString + joined
    joiner = ", and "
    finalString = finalString + joiner + lastTerm + "."
    return(finalString)


if __name__ == "__main__":
    #print(dayLunch(day = "3/4/2022", school="Dixon Middle"))
    #print(dayLunch("3/3/2022"))
    print(dayLunch())