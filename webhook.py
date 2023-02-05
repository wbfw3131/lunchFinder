from lunchfinder import dayLunch
from school import School
from menuTypes import *
from discord_webhook import DiscordWebhook
from urllib.parse import urlparse
from re import search
from os import abort, getenv
from sys import argv
import dotenv

#greenBulldogURL = "https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/998339/Green%20Collar%20Bulldog.png"
#normalBulldogURL = "https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/318015/bulldog.png"
#districtURL = "https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/547468/pcsd-logo-website-header-x2.png"
#fruitURL = "http://www.schoolnutritionandfitness.com/webmenus2/api/productController.php/img?filename=upload/fruit-107.jpg"
#provoWallpaperURL = "https://itsmealsprovo.com/district/pcs/layout/provo_wallpaper.jpg"
#dixonPawURL = "https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/547674/dixon.png"
#dixonHeaderURL = "https://dixon.provo.edu/wp-content/themes/dms-child/assets/images/header-logo.png"
#dixonPawIconURL = "https://dixon.provo.edu/wp-content/themes/dms-child/assets/images/favicon.png"
#timpviewLowQualIconURL = "https://timpview.provo.edu/wp-content/themes/timpview-child/assets/images/favicon.png"
#timpviewT = "https://timpview.provo.edu/wp-content/themes/timpview-child/assets/images/header-logo.png"
#centennialIconURL = "https://centennial.provo.edu/wp-content/themes/alyeska-child/favicon.png"
#westridgeWrongColorsIconURL = "https://westridge.provo.edu/wp-content/themes/westridge-child/assets/images/favicon.png"
#westridgeWildcatURL = "https://westridge.provo.edu/wp-content/themes/westridge-child/assets/images/header-logo.png"

def main(schoolName: str, webhookURL: str | None, menu: str | MenuTypes = MenuTypes.LUNCH, date: str = "today"):

    school = School(schoolName)
    if type(menu) != MenuTypes:
        menu = findMenu(menu)
    message = dayLunch(schoolStr=school, menu=menu, day=date)
    if not message.hasFood:
        print("There is no lunch that day, will not send a message")
        abort()
    
    #check to see if webhookURL is a valid Discord webhook link
    if type(webhookURL) == str:
        if urlparse(webhookURL).netloc=="discord.com" and urlparse(webhookURL).path.startswith("/api/webhooks/"):
            print("Webhook URL passed in, not checking environment variables")
        else:
            print("Webhook URL passed in doesn't seem valid, trying environment variables")
            webhookURL = getEnvVar()
    else:
        webhookURL = getEnvVar()
        

    webhook = DiscordWebhook(url=webhookURL, content=message.content)

    # embed = DiscordEmbed(title="Today's Lunch", description=message, color='32a852')
    # embed.set_author(name="Provo High Lunch", icon_url="https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/318015/bulldog.png")
    # embed.set_image(url="https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/318015/bulldog.png")
    webhook.avatar_url = school.iconURL
    webhook.username = school.name + f"'s {menu.name.title()}"

    webhook.execute()

def getEnvVar() -> str:
    # if os.DirEntry.is_file(os.path.join(os.path.dirname(__file__), ".env")):
    if dotenv.find_dotenv() != "":
        if dotenv.dotenv_values() != {}:
            dotenv.load_dotenv(override=True)
            print("Successfully loaded .env file")
        else:
            print("You have a .env file, but there's nothing defined inside")

    envVar = getenv("DISCORD_WEBHOOK_URL")
    if envVar == None:
        raise ValueError("Could not find an environment variable for the webhook URL")
    return envVar
    



if __name__ == "__main__":
    webhookLink = None

    # defaults
    menuType = MenuTypes.LUNCH
    date = "today"

    #remove unneeded arg
    argv.pop(0)

    if len(argv) == 0:
        schoolStr = input("What is the name of the school you want to know the lunch of? ")
    else:
        for arg in argv.copy():

            # check if date
            matchTest = search("today|tomorrow|(.{2}|.{1})\/(.{2}|.{1})\/(.{4}|.{2})", arg.lower())
            if matchTest:
                date = arg[matchTest.start():matchTest.end()]
                argv.remove(arg)
                continue

            # check if webhook link
            testURL = urlparse(arg)
            if testURL.netloc=="discord.com" and testURL.path.startswith("/api/webhooks/"):
                webhookLink = arg
                argv.remove(arg)
                continue

            # check if menu
            for menu in MenuTypes:
                if arg.lower().find(menu.name.lower()) != -1:
                    menuType = menu
                    argv.remove(arg)
                    break

        # make school from remaining args
        schoolStr = " ".join(argv[0:])

    main(schoolStr, webhookLink, menuType, date)
