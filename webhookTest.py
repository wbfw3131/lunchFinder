#from urllib import response
from lunchfinder import dayLunch
from discord_webhook import DiscordWebhook, DiscordEmbed
import json

#greenBulldogURL = "https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/998339/Green%20Collar%20Bulldog.png"
#normalBulldogURL = "https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/318015/bulldog.png"
#districtURL = "https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/547468/pcsd-logo-website-header-x2.png"
#fruitURL = "http://www.schoolnutritionandfitness.com/webmenus2/api/productController.php/img?filename=upload/fruit-107.jpg"
#provoWallpaperURL = "https://itsmealsprovo.com/district/pcs/layout/provo_wallpaper.jpg"

def main():
    message = dayLunch()

    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/948615440295419995/B3pEFTSZe2342e2q29uX8Kpki4wCrt-ZJ5QMCeOAREWPBJFLEhrwl0LEVpUb5n0sXgjU', content=message)

    # embed = DiscordEmbed(title="Today's Lunch", description=message, color='32a852')
    # embed.set_author(name="Provo High Lunch", icon_url="https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/318015/bulldog.png")
    # embed.set_image(url="https://instructure-uploads.s3.amazonaws.com/account_17190000000000001/attachments/318015/bulldog.png")


    response = webhook.execute()
    # deleteLast(webhook)
    # storeNew(response)


def deleteLast(webhook: DiscordWebhook):
    f = open('lastMessage.json')
    data = json.load(f)
    lastMessage = data['lastMessage']
    webhook.delete(lastMessage)

def storeNew(webhook: DiscordWebhook):
    f = open('lastMessage.json', 'w')
    f.write(json.dumps({'lastMessage': webhook}))

if __name__ == "__main__":
    main()