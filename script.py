from bs4 import BeautifulSoup
import requests
from datetime import timedelta
import re
import sys

args = sys.argv
url = sys.argv[1]

pattern = re.compile('https://www.youtube.com/playlist?')
if not pattern.match(url):
    raise SyntaxError('Enter a valid URl')

ret_obj = requests.get(url)

soup = BeautifulSoup(ret_obj.content, 'lxml')

if soup.find('h1', class_="pl-header-title") == None:
    raise SyntaxError('Enter a valid URL')
else:
    title = soup.find('h1', class_="pl-header-title").text
    channel = soup.find('ul', class_="pl-header-details")
    channel = channel.find('a').text
    vid_time_obj = soup.find_all(class_='timestamp')
    search_1 = soup.find('ul', class_='pl-header-details')
    li_search = search_1.find_all('li')
    li_list = [element.text for element in li_search]
    vid_times = [element.text for element in vid_time_obj]

    hrs = 0
    mins = 0
    secs = 0
    for element in vid_times:
        try:
            temp_mins, temp_secs = element.split(':')
            temp_hrs = 0
        except ValueError:
            temp_hrs, temp_mins, temp_secs = element.split(':')
        temp_hrs = int(temp_hrs)
        temp_mins = int(temp_mins)
        temp_secs = int(temp_secs)
        hrs += temp_hrs
        mins += temp_mins
        secs += temp_secs

    num_vids = len(vid_time_obj)
    total_secs = 3600 * hrs + 60 * mins + secs
    avg_secs = round(total_secs / num_vids)
    duration = timedelta(hours=hrs, minutes=mins, seconds=secs)
    avg_duration = timedelta(seconds=avg_secs)
    print('\nPlaylist: ', title.strip())
    print('Channel: ', channel)
    print('No. of videos: ', num_vids)
    print('Total playlist duration: ', duration)
    print('Average video duration: ', avg_duration)
    print(li_list[2])
