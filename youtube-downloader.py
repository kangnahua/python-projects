"""
A Python program to download YouTube videos on the first search page
Inspiration from Tafarel Yan, and special thanks to BeautifulSoup and YouTube-DL
Author: Nahua Kang
"""
from __future__ import unicode_literals
import youtube_dl

from bs4 import BeautifulSoup
from urllib.request import urlopen

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }

# query: query for a song keyword and returns the url to be read
def query():
    query = input('Please enter the name of the song: ')

    if len(query.split()) > 1:
        query = '+'.join(query.split())
    # return url
    return "https://www.youtube.com/results?search_query=" + query

# soupTags: using Beautifulsoup 
def soupTags(url):
    content = urlopen(url).read()
    # set parser to "lxml"
    soup = BeautifulSoup(content, "lxml")

    title_tags = soup.findAll('a', {'rel':'spf-prefetch'})
    view_tags = soup.findAll('ul', {'class':'yt-lockup-meta-info'})
    return title_tags, view_tags

# songList: creating a dictionary listing songs from the first page of YouTube search query
def songList(title_tags, view_tags):
    songDict = {}
    for i in range(len(title_tags)):
        title = title_tags[i].text
        video_url = "https://www.youtube.com"+title_tags[i].get('href')
        if len(view_tags[i]('li')) == 2:
            view_raw = view_tags[i]('li')[1].text
        elif len(view_tags[i]('li')) == 1:
            view_raw = view_tags[i]('li')[0].text
        view, _ = view_raw.replace("\xa0",'').split(' ')
        songDict[title] = {video_url:int(view)}
    return songDict

# displaySongs: displaying all the choices for user to select
def displaySongs(songDict):
    displayList = []
    for key1 in songDict.keys():
        displayList.append(key1)
        for key2 in songDict[key1]:
            print("{} {}: {:,} views".format(len(displayList), key1, songDict[key1][key2]))
    return displayList

# selectSong: user chooses the song to be downloaded, download url is returned
def selectSong(displayList, songDict):
    print("Please enter the number in the list for the song you want: ", end='')

    isNum = False
    while not isNum:
        try:
            number = int(input())
            isNum = True
        except ValueError:
            print("Please enter a number for the song you want to download: ", end='')
    downloadTitle = displayList[number - 1]
    downloadUrl = list(songDict[downloadTitle].keys())[0]
    print("Your choice is: {} {}".format(number, downloadTitle))
    return downloadTitle, downloadUrl



if __name__ == "__main__":
    url = query()
    title_tags, view_tags = soupTags(url)
    songDict = songList(title_tags, view_tags)
    displayList = displaySongs(songDict)
    downloadTitle, downloadUrl = selectSong(displayList, songDict)
    print("Downloading title {} from {}......".format(downloadTitle, downloadUrl))

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([downloadUrl])
