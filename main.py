from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import discord
from discord.ext import tasks
import time
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not DISCORD_BOT_TOKEN:
    raise Exception("Discord bot token not found in .env file")
CHANNEL_ID = "969024140206043147"
OWNER_ID = "285889916225847296"

MOVIE_LINK = "https://www.cineplex.com/movie/oppenheimer-the-imax-experience-in-70mm-film"
THEATRE_NAME = "Cineplex Cinemas Mississauga"


def get_dates(verbose: bool = False) -> list[datetime]:
    driver = webdriver.Chrome()
    driver.get(MOVIE_LINK)
    driver.execute_script("return navigator.webdriver")
    
    button = driver.find_element(By.XPATH, '//button[@data-name="get-tickets" and contains(text(), "Get Tickets")]')
    button.click()
    time.sleep(5)

    select_theatre_button = driver.find_element(By.XPATH, '//button[@data-name="select-Theatre"]')
    select_theatre_button.click()
    time.sleep(5)

    # input_box = driver.find_element(By.NAME, "filter-movies")
    # input_box.send_keys(THEATRE_NAME)
    # time.sleep(5)
    # press enter
    # input_box.send_keys(Keys.RETURN)
    # time.sleep(5)

    cinemas_button = driver.find_element(By.XPATH, '//button[@aria-label="' + THEATRE_NAME + '"]')
    cinemas_button.click()
    time.sleep(5)

    select_date_button = driver.find_element(By.XPATH, '//button[@data-name="select-Date"]')
    select_date_button.click()
    time.sleep(5)

    dates = []
    date_buttons = driver.find_elements(By.XPATH, '//button[starts-with(@data-name, "date-")]')
    for button in date_buttons:
        date_span = button.find_element(By.XPATH, './/span')
        date_str = date_span.text
        date_obj = datetime.strptime(date_str, '%B %d, %Y')
        dates.append(date_obj)
    
    driver.quit()
    return dates

def spin_discord_bot():
        
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(DISCORD_BOT_TOKEN)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        self.check_dates.start()

    @tasks.loop(seconds=60)
    async def check_dates(self):
        try:
            dates = get_dates()
            print("Got dates: " + str(dates))
            latest_date = max(dates)
            if latest_date.date() > datetime(2021, 7, 26).date():
                channel = self.get_channel(int(CHANNEL_ID))
                await channel.send("<@!" + OWNER_ID + "> Oppenheimer is available on " + latest_date.strftime("%B %d, %Y")) # type: ignore
        except Exception as e:
            channel = self.get_channel(int(CHANNEL_ID))
            await channel.send("Error occurred while checking dates: " + str(e))  # type: ignore

spin_discord_bot()
