#!/usr/bin/env python3
# Download every ForoCoches emote
# A hug strong

from bs4 import BeautifulSoup
import os
import requests

URL = "https://www.forocoches.com/foro/misc.php"
DOWNLOAD_ROUTE = "gifs/" 

# Convenience class for emote data
class Emote:
    def __init__(self, name, url):
        self.name = name
        self.url = url


# Get every emote's name and URL
def getEmotes():
    emotes = []
    # Gets root emote page
    resp = requests.get(URL)
    html = BeautifulSoup(resp.text, "html.parser")
    # There are no HTML classes/ids, so this will be quite horrid
    # Get every tr with 3 td children and a central image
    trs = html.find_all("tr", {"align": "center"})
    trs = [tr for tr in trs if len(tr.find_all("td", recursive=False)) == 3]
    trs = [tr for tr in trs if tr.find_all("td", recursive=False)[1].img is not None]
    for tr in trs:
        tds = tr.find_all("td")
        # Gets emote's name, deletes spaces and .
        name = tds[1].img["alt"].replace(" ", "").replace(".", "")
        for x in filter(lambda x: not (x.isalnum() or " " in x), name):
            print(f"Filtered out: {x}")
        # Gets emote's URL (adds "http:" if not there already)
        url = tds[1].img['src']
        if not url.startswith("http"):
            url = f"http:{tds[1].img['src']}"
        # Adds to list
        emotes.append(Emote(name, url))
    return emotes


# Downloads and saves every emote in ${emoteList}
def downloadEmotes(emoteList):
    for emote in emoteList:
        fileName = f"{DOWNLOAD_ROUTE}{emote.name}.gif"
        if not os.path.exists(fileName):
            with open(fileName, "wb") as file:
                resp = requests.get(emote.url)
                file.write(resp.content)
        else:
            print(f"Already exists: {fileName} ({emote.url})")


if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_ROUTE):
        os.makedirs(DOWNLOAD_ROUTE)
    emotes = getEmotes()
    downloadEmotes(emotes)
