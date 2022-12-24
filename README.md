# lunchFinder
My method of getting what's for lunch at school and delivering it via a Discord webhook

## Setup
To install the required dependencies, run:
```shell
pip install -r requirements.txt
```

To setup Discord webhook functionality, either:
- add your webhook URL as an environment variable named `DISCORD_WEBHOOK_URL` to your system, or

- rename `example.env` to just `.env`, remove the comments, and add your link to the file like this:

```
DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/...
```
> Variables in the `.env` file take precedence over system environment variables

## Usage

After setup, you can run [lunchfinder.py](lunchfinder.py) and [webhook.py](webhook.py) by themselves and they will ask for the proper arguments. [webhook.py](webhook.py) also accepts command-line arguments for school names and webhook URLs. Here are some examples of valid calls:
```shell
python webhook.py Cool High School    #defaults to environment URL

python webhook.py Nice Middle School https://discord.com/api/webhooks/...    #uses URL passed in
```


## Special Thanks
Shout out to [shepgoba](https://github.com/shepgoba) for figuring out how to make the API requests