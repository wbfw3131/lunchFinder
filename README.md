# lunchFinder
My method of getting what's for lunch at school and delivering it via a Discord webhook

## Setup
To install the required dependencies, run:
```
pip install -r requirements.txt
```
> Note: At the moment, the dependencies are only required for the Discord webhook functionality

To setup Discord webhook functionality, either add your webhook URL as an environment variable named `DISCORD_WEBHOOK_URL` on your system or rename `example.env` to just `.env`, remove the comments, and add your link to the file like this:
```
DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/...
```

## Special Thanks
Shout out to [shepgoba](https://github.com/shepgoba) for figuring out how to make the API requests