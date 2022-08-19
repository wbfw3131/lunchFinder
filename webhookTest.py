from lunchfinder import dayLunch
from school import School
from discord_webhook import DiscordWebhook, DiscordEmbed
import os, sys
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

def main(schoolName: str):

    school = School(schoolName)
    message = dayLunch(schoolStr=school)
    
    # if os.DirEntry.is_file(os.path.join(os.path.dirname(__file__), ".env")):
    if dotenv.find_dotenv() != "":
        if dotenv.dotenv_values() != {}:
            dotenv.load_dotenv()
            print("Successfully loaded .env file")
        else:
            print("You have a .env file, but there's nothing defined inside")

    webhookURL = os.getenv("DISCORD_WEBHOOK_URL")
    if webhookURL == None:
        raise RuntimeError("Could not find an environment variable for the webhook URL")

    webhook = DiscordWebhook(url=webhookURL, content=message)

    # embed = DiscordEmbed(title="Today's Lunch", description=message, color='32a852')
    # embed.set_author(name="Provo High Lunch", icon_url="https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/318015/bulldog.png")
    # embed.set_image(url="https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/318015/bulldog.png")
    webhook.avatar_url = school.imageURL
    webhook.username = school.name + "'s Lunch"

    response = webhook.execute()
    # deleteLast(webhook)
    # storeNew(response)



if __name__ == "__main__":
    if len(sys.argv) == 1:
        schoolStr = input("What is the name of the school you want to know the lunch of? ")
    else:
        schoolStr = " ".join(sys.argv[1:])

    main(schoolStr)
