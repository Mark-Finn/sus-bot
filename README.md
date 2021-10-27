# sus-bot
Discord bot to GM in person Among Us games


# Dependencies:
1. Python 3 or better
2. discord.py https://pypi.org/project/discord.py/
3. discord-components.py https://pypi.org/project/discord-components/
4. Pillow https://pypi.org/project/Pillow/

# Bot Setup:
0. Install dependencies above
1. Create an application https://discord.com/developers/applications
2. Go to Bot and create a bot for your application
3. Under Privileged Gateway Intents, check PRESENCE INTENT and SERVER MEMBERS INTENT
4. Under Bot Bot Permissions, add Administrator
5. Go to OAuth2 > SCOPES > Select bot > BOT PERMISSIONS > Administrator > Copy link
6. Visit copied link and add bot to your Discord server

# Code Setup:
1. Fill out all fields in cofig.py
2. Run main.py
3. Use .help to see commands available
