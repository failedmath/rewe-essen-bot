# rewe-essen-bot
Women and Code hackathon

A Telegram bot that allows you to fetch a recipe from Edamam database, parse the ingredients, pick the missing ones and create a  shopping list.
The idea was supporting a Rewe track at the Women and Code hackathon with topic: "Improving online shopping experience".
Basically, it is just an example of using a Telegram bot, and more feasible version would be a normal App.

Ideas for improvement to create MVP:
- Have an app instead of Telegram Bot
- Add a payment method (Telegram also supports Apple Pay and Android Pay)
- Connect to REWE online store
- Be able to remove foods from the list
- Add allergies or not tasty foods
- Add prices and choices 
- Use official REWE “Deine Küche”
- Choose one of multiple seasonal recipes & save recipes
- Add voice control


Check requirements.txt file for dependencies. 
Create a .env file with three parameters: ACCESS_TOKEN for telegram bot (need to write to @BotFather on telegram for that), API_ID and API_KEY from  https://developer.edamam.com/edamam-docs-recipe-api for recipe fetching.
