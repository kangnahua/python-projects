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


query = input('Please enter the name of the song: ')

if len(query.split()) > 1:
    query = '+'.join(query.split())

url = "https://www.youtube.com/results?search_query=" + query
content = urlopen(url).read()
# set parser to "lxml"
soup = BeautifulSoup(content, "lxml")

title_tags = soup.findAll('a', {'rel':'spf-prefetch'})
view_tags = soup.findAll('ul', {'class':'yt-lockup-meta-info'})

# dict {title:{url:view}}
# store information into dict
dict = {}
for i in range(len(title_tags)):
    title = title_tags[i].text
    video_url = "https://www.youtube.com" + title_tags[i].get('href')

    if len(view_tags[i]('li')) == 2:
        view_raw = view_tags[i]('li')[1].text
    elif len(view_tags[i]('li')) == 1:
        view_raw = view_tags[i]('li')[0].text

    view, _ = view_raw.replace('\xa0', '').split(' ')
    dict[title] = {video_url:int(view)}

# print out the top 19 search results from YouTube
title_list = []
for key1 in dict.keys():
    title_list.append(key1)
    for key2 in dict[key1]:
        print("{} {}: {:,} views".format(len(title_list), key1, dict[key1][key2]))

print("Please enter the song you want to download: ", end='')

isNum = False
while not isNum:
    try:
        number = int(input())
        isNum = True
    except ValueError:
        print("Please enter a number for the song you want to download: ", end='')
        #isNum = False
print("Your choise is: {} {}".format(number, title_list[number - 1]))

download_title = title_list[number - 1]
download_url = list(dict[download_title].keys())[0]
print("Downloading title {} and url {}......".format(download_title, download_url))

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([download_url])
