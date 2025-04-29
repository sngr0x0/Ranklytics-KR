from playwright.sync_api import sync_playwright
import argparse
import pandas as pd
import sys
import os

parser = argparse.ArgumentParser(
    prog= os.path.basename(sys.argv[0]), # Program Name
    usage= "%(prog)s [options]", # Usage
    description= "This is a program that scrapes live tier changes for korean LOL pro players.", # Description
    epilog= "python %(prog)s -i" # How to run it
)
parser.add_argument(
    '-i', 
    '--interval', 
    help= 'The interval over which we\'re getting tier changes.',
    required=True,
    choices=['m', 'd', 'w']
    )
# m -> month
# d -> day
# w -> week
args = parser.parse_args()

with sync_playwright() as p:
    daily_improvement = f"{os.getcwd()}/daily_improvement.csv"
    weekly_improvement = f"{os.getcwd()}/weekly_improvement.csv"
    monthly_improvement = f"{os.getcwd()}/monthly_improvement.csv"

    if args.interval == 'm':
        url = f'https://op.gg/lol/spectate/live/tier-changes?period=month'
        sheet_path = monthly_improvement
    elif args.interval == 'd':
        url = f'https://op.gg/lol/spectate/live/tier-changes?period=day'
        sheet_path = daily_improvement
    else:
        url = f'https://op.gg/lol/spectate/live/tier-changes?period=week'
        sheet_path = weekly_improvement


    # Launch the browser and open a new page
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    try:
        # Navigate to the constructed URL
        page.goto(url, timeout = 60000)
    except Exception as e:
        print("Can't navigate to the provided URL.\nExitting...")
        sys.exit()

    page.wait_for_selector("tbody>tr", timeout=30000)
    players = page.locator('tbody>tr').all()
    # page.keyboard.press("End")

    print(len(players))

    players_list = []
    for idx, player in enumerate(players):
        # if idx == 5:
        #     break
        print(f"scraping player {idx + 1}")
        player_dict = {}
        # Find player name
        try:
            # player_dict['id'] = player.locator(".whitespace-pre-wrap.text-gray-900.\!truncate.font-bold").inner_text(timeout=500)
            player_dict['id'] = player.locator(".flex.items-center.gap-1.truncate").inner_text(timeout=700).replace('\n', '')
        except Exception:
            player_dict['id'] = 'N/A'

        try:
            # if player.locator(".hidden.md\:block.md\:truncate").is_visible(timeout=1000):
            #     player_dict['team'] = player.locator(".hidden.md\:block.md\:truncate").inner_text(timeout=1000)
            if player.locator(".flex.items-center.gap-1.text-2xs.text-gray-500").is_visible(timeout=700):
                player_dict['team'] = player.locator(".flex.items-center.gap-1.text-2xs.text-gray-500").inner_text(timeout=700).replace('\n', ' ')
                # flex items-center gap-1 text-2xs text-gray-500
        except Exception:
            player_dict['team'] = 'N/A'
        
        # This step consumed too much time because many rows doesn't have red or green elements.
        # In such cases, it would wait until they timeout automatically, causing a waiting interval of about 60 seconds.
        # Too much lag!
        try:
            if player.locator(".text-green-600").is_visible(timeout=700):
                player_dict['gained_lp']= int(player.locator(".text-green-600").inner_text(timeout=700))
            elif player.locator(".text-red-600").is_visible(timeout=700):
                player_dict['gained_lp']= -int(player.locator(".text-red-600").inner_text(timeout=700))
            else:
                player_dict['gained_lp']= 0
        except:
            player_dict['gained_lp']= 'N/A'
        
        try:
            player_dict['interval_winrate'] = player.locator(".basis-7.text-2xs").inner_text(timeout=700)
        except Exception:
            player_dict['interval_winrate'] = 'N/A'
        players_list.append(player_dict)

    df = pd.DataFrame(players_list)
    df.to_csv(sheet_path, index= False)

    browser.close()
                