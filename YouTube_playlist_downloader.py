import requests
import urllib.request
from bs4 import BeautifulSoup
#url = 'https://www.youtube.com/watch?v=S86QnrME6Fs&list=PLAwxTw4SYaPlRyoU4luNRaviHScla_nzM'

def keepvid_download_link(start=1 , end=300):
    fr = open('links.txt', 'r')
    links = fr.read()
    links = links.split("\n")
    fkeep = open('keepvid.txt', 'w')
    n=1
    for link in links:
        if n>=start and n<=end:
            if link != "":
                keepvid_url = 'http://keepvid.com/?url=' + link
                # print(keepvid_url)
                href = download_link(keepvid_url)
                print(href)
                fkeep.write(href + "\n")
        n+=1
        if n>end:
            break
    fkeep.close()
    fr.close()

def downloading( num, user_input = 0):
    print('Downloading....')
    fr_title = open('vid_title.txt', 'r')
    titles = fr_title.read()
    titles = titles.split("\n")
    fr_link = open('keepvid.txt', 'r')
    links = fr_link.read()
    links = links.split("\n")
    max_index = len(links)-1
    if user_input == 0:
        user_input = num
    #print(len(titles))

    for link in links:
        if num < (max_index+1):
            if link[num-1] is not "no video found":

                #print(link[num-1])
                download_vid(links[num - 1], titles[user_input - 1])
                print(titles[user_input-1] + "  --Downloaded")
            else:
                print(titles[user_input-1] + "  --Download Failed")

        num += 1
        user_input+=1

    fr_link.close()
    fr_title.close()
    print("Download Complete.")


def download_vid(link, title):
    name =str(title) + ".mp4"
    urllib.request.urlretrieve(link,name)


def download_link(url):
    source = requests.get(url)
    plain_text = source.text
    soup = BeautifulSoup(plain_text)
    #print('yes')

    a = 0
    c=0
    k=0

    for row in soup.findAll('td'):

        qulity = str(row.string)
        #print(qulity)
        a+=1;
        if qulity == '(Max 720p)':
            c=((a-1)/4)+1
            for link in soup.findAll('a', {'class': 'btn-outline'}):
                k+=1
                #print(k)
                if k == c:
                    href = link.get('href')
                    #print(href)
                    return href



                    break
        elif qulity == '480p':
            c = ((a - 1) / 4) + 1
            for link in soup.findAll('a', {'class': 'btn-outline'}):
                k += 1
                # print(k)
                if k == c:
                    href = link.get('href')
                    # print(href)
                    return href
                    break


        if k > 0 :

            break
    return 'no video found'

def download_link_youtube(url):
    source = requests.get(url)
    plain_text = source.text
    soup = BeautifulSoup(plain_text)
    fw = open('links.txt', 'w')
    for link in soup.findAll('a', {'class': 'playlist-video'}):
        href =  'https://www.youtube.com' + link.get('href')

        fw.write(href+"\n")

    fw.close()
    fw1 = open('vid_title.txt', 'w')
    index=1
    for title in soup.findAll('h4', {'class': 'yt-ui-ellipsis'}):
        title_vid = title.string
        title_vid=str(index)+"."+title_vid.strip()
        fw1.write(title_vid + "\n")
        index+=1

    fw1.close()





print("Select your option : \nEnter 1 : To download playlist (Complete) form url\nEnter 2 : To resume your download.\nEnter 3 : For custom download")
option = input('Enter your option : ')
if option is '1':
    url = input('Enter URL of any video of Youtube Playlist : ')
    download_link_youtube(url)
    keepvid_download_link()
    starting_index = 1
    downloading(starting_index)
if option is '2':
    starting_index =int( input('Enter the video number to start download from  : '))
    downloading(starting_index)
if option is '3':
    url = input('Enter URL of any video of Youtube Playlist : ')
    starting_index = int(input('Enter the video number to start download from  : '))
    ending_index = int(input('Enter the video number to end at  : '))
    download_link_youtube(url)
    keepvid_download_link(starting_index, ending_index)
    downloading(1,starting_index)
