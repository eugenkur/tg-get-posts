import configparser
from telethon import TelegramClient
import sys
import os
#import requests

#Пример вызова скрипта:
#python getPosts.py 143 https://t.me/necn123/198 1000 5
    #1. id = id заказа из параметров консольки
    #2. url = ссылка на пост из параметров консольки
    #3. cheatAmount = кол-во просмотров из параметров консольки
    #4. postsAmount = кол-во добавочных постов из параметров консольки

#cd /var_tg-view/requests
#python3 /var_tg-view/requests/getPosts.py 23 https://t.me/necn123/417 10000 9

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)

async def main():

    getId = sys.argv[1]
    getUrl =str(sys.argv[2])
    getCheatAmount = sys.argv[3]
    getPostsAmount = int(sys.argv[4])

    urlArr = getUrl.split("/")
    
    channelName = urlArr[3]

    posts_id = []
    print('start')
    curent_id = int(urlArr[4]) + 1
    grouped_id_check = ""
    while(len(posts_id)<=getPostsAmount):
        posts = await client.get_messages(urlArr[3], 1, max_id = curent_id)
        if posts[0].grouped_id==None:
            posts_id.append(posts[0].id)
        else:
            if(posts[0].grouped_id != grouped_id_check):
                posts_id.append(posts[0].id)
                grouped_id_check = posts[0].grouped_id
        curent_id = posts[0].id
        #print(curent_id)
        if curent_id == 1:
            #print("Хуй наебешь, посты кончились")
            break
    id_list = ""
    for i in range(0, len(posts_id)):
        id_list += str(posts_id[i])
        if i == len(posts_id)-1:
            break
        id_list += ":"
    
    #sendData = 'https://tg-view.ru/server_api/getPostsForCheat.php?postsArr='+id_list
    #response = requests.get(sendData)
    #print(response.text)
    
    #print(posts_id)
    print("********** Finish check **********")
    '''
    print("getId:", getId)
    print("getPostsAmount:", getPostsAmount)
    print("getCheatAmount:", getCheatAmount)
    print("Posts array:", id_list)
    print("Channel name:", channelName)
    '''
    command = "./some_posts -id=" + str(getId) + " -channel=" + str(channelName) + " -amount=" + str(getCheatAmount) + " -posts=" + id_list #command to be executed 
    res = os.system(command) #the method returns the exit status 
    print("Returned Value: ", res)
    

with client:
    client.loop.run_until_complete(main())