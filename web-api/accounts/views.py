from django.shortcuts import render 
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpRequest , HttpResponse , JsonResponse
from django.shortcuts import redirect
import requests
from django.contrib.auth import authenticate , login
from .models import CustomUser
import string
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from django.contrib import messages

# Create your views here.

redirect_url = "https://discord.com/oauth2/authorize?client_id=1267853009476386897&response_type=code&redirect_uri=https%3A%2F%2F127.0.0.1%3A8000%2Fauth2%2Fdiscord%2Flogin%2F&scope=identify+guilds+gdm.join+rpc.notifications.read+email+guilds.join+guilds.members.read+connections+gateway.connect"
redirect2 = "https://discord.com/oauth2/authorize?client_id=1267853009476386897&response_type=code&redirect_uri=https%3A%2F%2F127.0.0.1%3A8000%2Fauth2%2Fdiscord%2Flogin%2F&scope=identify+guilds"
redirect3 = "https://discord.com/oauth2/authorize?client_id=1267853009476386897&permissions=2048&response_type=code&redirect_uri=https%3A%2F%2F127.0.0.1%3A8000%2Fauth2%2Fdiscord%2Flogin%2F&integration_type=0&scope=identify+guilds+bot"
redirect4 = "https://discord.com/oauth2/authorize?client_id=1267853009476386897&permissions=2048&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fauth2%2Fdiscord%2Flogin%2Fredirect&integration_type=0&scope=identify+guilds+bot"
redirect_login = "https://discord.com/oauth2/authorize?client_id=1267853009476386897&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fauth2%2Fdiscord%2Flogin%2Fredirect&scope=identify+guilds"
####################

API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1267853009476386897'
CLIENT_SECRET = 'l67Q05jVqQi2JKroZ-9ahaYxDHLKKKe7'
REDIRECT_URI = 'http://127.0.0.1:8000/auth2/discord/login/redirect'

cluster = MongoClient("url")
# Send a ping to confirm a successful connection
db = cluster["add"]
collection = db["add"]
collection_total = db['servers']

#################
def discordLogin (request):
    return redirect(redirect4)

def successRedirect(request):
    code = request.GET.get('code')
    # print(code)
    user , guilds  , bot_guilds = analyze_code(code)
    random_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    try:
        user1 = CustomUser.objects.get(discord_id = user['id'])
    except:
        user1=CustomUser.objects.create(discord_id = user['id'] ,discord_tag=user['username'],avatar=user['avatar'],public_flags=user['public_flags'] , flags=user['flags'],locale=user['locale'],mfa_enabled=user['mfa_enabled'], username = user['username'] , password = make_password(random_password) , )

    login(request , user1)
    # print(guilds)
    # print(channels[0]['name'])
    request.session['servers'] = guilds
    request.session['bot_servers'] = bot_guilds
    return redirect('profileView')


def analyze_code(code):
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        "scope":'identity guilds'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    answer = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))

    access_token = answer.json()['access_token']

    print(access_token)

    response = requests.get("https://discord.com/api/v6/users/@me" , headers={
        'Authorization': f"Bearer {access_token}"
    })
    response2 = requests.get("https://discord.com/api/v6/users/@me/guilds" , headers={
        'Authorization': f"Bearer {access_token}"
    })
    # response3 = requests.get("https://discord.com/api/v6/guilds/1198003051919855737/channels" , headers={
    #     'Authorization': f"Bot MTI2Nzg1MzAwOTQ3NjM4Njg5Nw.GEngSz.sKoQgCseG1ySMunYaOBHGmbQ5H0xkp0zvwckns"
    # })

    response4 = requests.get(f"https://discord.com/api/v6/users/@me/guilds" , headers={
        'Authorization': f"Bot MTI2Nzg1MzAwOTQ3NjM4Njg5Nw.GEngSz.sKoQgCseG1ySMunYaOBHGmbQ5H0xkp0zvwckns"
    })


    return response.json() , response2.json()  , response4.json()

@login_required()
def profileView(request):
    selected_value = None
    channels = None
    tabadol_lists = ['همه دسته ها','پابلیک' , 'بازی' , 'موزیک' , 'انیمیشین' , 'برنامه نویسی' , 'فیلم' , 'پلاتو' ,'فروشگاه']
    genres_list = ['پابلیک' , 'بازی' , 'موزیک' , 'انیمیشین' , 'برنامه نویسی' , 'فیلم' , 'پلاتو' ,'فروشگاه']
    anime_guilds = None
    public_guilds = None
    development_guilds = None
    movie_guilds = None
    game_guilds = None
    platto_guilds = None
    music_guilds = None
    shop_guilds = None

    is_true= False
    channel_selected_name = None
    is_done = False
    if request.method =="POST":
        
        request.session['selected'] = request.POST['dropdown']
        
        selected_value = request.session['selected']
        guilds = request.session['servers']
        bot_guilds = request.session['bot_servers']
        my_temp_ids = {}
        for j in bot_guilds:
            for i in guilds:
                if j['id'] == i['id']:
                    if i['owner'] == True:
                        my_temp_ids[f"{i['name']}"] = i['id']
        
        guild_id = my_temp_ids[f'{selected_value}']
        is_done = True
        try:
            if request.POST['channels'] == "" or request.POST['category'] == '' or request.POST['tabadol'] == "" or request.POST['title_banner'] == "" or request.POST['body_banner'] == "" or request.POST['link_banner'] == '':
                messages.warning(request , 'همه ی کادرهارا پر کنید')
            else:
                if (find:=collection.find_one({'server_id':int(guild_id)})):
                    anime_guilds = []
                    public_guilds = []
                    development_guilds = []
                    movie_guilds = []
                    game_guilds = []
                    platto_guilds = []
                    music_guilds = []
                    shop_guilds = []
                    if (find2:=collection_total.find_one({'totality':1})):
                        total_sv = find2['all_guilds']
                        if guild_id not in total_sv:
                            total_sv.append(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"all_guilds":total_sv}})

                            anime_guilds = find2['anime_guilds']
                            public_guilds = find2['public_guilds']
                            development_guilds = find2['development_guilds']
                            movie_guilds = find2['movie_guilds']
                            game_guilds = find2['game_guilds']
                            platto_guilds = find2['platto_guilds']
                            music_guilds = find2['music_guilds']
                            shop_guilds = find2['shop_guilds']

                    else:
                        tmp_guild = []
                        tmp_guild.append(guild_id)
                        collection_total.insert_one({'totality':1,"all_guilds":tmp_guild,"anime_guilds":[],"public_guilds":[],"development_guilds":[],"movie_guilds":[] , "game_guilds":[],"platto_guilds":[],"music_guilds":[] , 'shop_guilds':[]})

                    response3 = requests.get(f"https://discord.com/api/v6/guilds/{guild_id}/channels" , headers={
                        'Authorization': f"Bot MTI2Nzg1MzAwOTQ3NjM4Njg5Nw.GEngSz.sKoQgCseG1ySMunYaOBHGmbQ5H0xkp0zvwckns"
                    })

                    request.session['channel_details'] = response3.json()


                    channels_db=request.session['channel_details']
                    id_selected_channel = None
                    for i in channels_db:
                        if i['type'] == 0:
                            if i['name'] == request.POST['channels']:
                                id_selected_channel = i['id']

                    genres = []
                    tabadol_value = 0
                    if request.POST['category'] == "پابلیک":
                        print('33')
                        genres.append(1)
                        public_guilds.append(guild_id)
                        collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        print('333')
                        if guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})

                    elif request.POST['category'] == "موزیک":
                        genres.append(2)
                        music_guilds.append(guild_id)
                        collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        if guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in public_guilds:
                            public_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})


                    elif request.POST['category'] == "بازی":
                        genres.append(3)

                        game_guilds.append(guild_id)
                        collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        if guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})



                    elif request.POST['category'] == "پلاتو":
                        genres.append(4)

                        platto_guilds.append(guild_id)
                        collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        if guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})




                    elif request.POST['category'] == "انیمیشن":
                        genres.append(5)
                        anime_guilds.append(guild_id)

                        collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        if guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})




                    elif request.POST['category'] == "فیلم":
                        genres.append(6)
                        movie_guilds.append(guild_id)


                        collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        if guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})



                    elif request.POST['category'] == "برنامه نویسی":
                        genres.append(7)
                        development_guilds.append(guild_id)


                        collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        if guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})




                    elif request.POST['category'] == "فروشگاه":
                        #### update genre
                        genres.append(8)
                        #####
                        shop_guilds.append(guild_id)
                        #update genre in total db
                        collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})
                        if guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})



                    
                    
                    ######################tabadol values ###################
                    

                    if request.POST['tabadol'] == "پابلیک":
                        print(66666666)
                        tabadol_value = 1
                    elif request.POST['tabadol'] == "موزیک":
                        tabadol_value = 2
                    elif request.POST['tabadol'] == "بازی":
                        tabadol_value = 3
                    elif request.POST['tabadol'] == "پلاتو":
                        tabadol_value = 4
                    elif request.POST['tabadol'] == "انیمیشن":
                        tabadol_value = 5
                    elif request.POST['tabadol'] == "فیلم":
                        tabadol_value = 6
                    elif request.POST['tabadol'] == "برنامه نویسی":
                        tabadol_value = 7
                    elif request.POST['tabadol'] == "فروشگاه":
                        tabadol_value = 8
                    elif request.POST['tabadol'] == "همه دسته ها": 
                        print('555555555555')
                        tabadol_value = "all"


                    ########################################################
                    if id_selected_channel !=None:
                        collection.update_one({"server_id":int(guild_id)} ,{"$set":{ 'channel':int(id_selected_channel) ,'banner_body':request.POST['body_banner'] , 'banner_title':request.POST['title_banner'] , 'banner_link':request.POST['link_banner'] , 'genres':genres , "active":True , 'tabadol':str(tabadol_value) , "tabadol_channels":[] }})


                else:
                    anime_guilds = []
                    public_guilds = []
                    development_guilds = []
                    movie_guilds = []
                    game_guilds = []
                    platto_guilds = []
                    music_guilds = []
                    shop_guilds = []
                    if (find2:=collection_total.find_one({'totality':1})):
                        total_sv = find2['all_guilds']
                        if guild_id not in total_sv:
                            total_sv.append(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"all_guilds":total_sv}})

                            anime_guilds = find2['anime_guilds']
                            public_guilds = find2['public_guilds']
                            development_guilds = find2['development_guilds']
                            movie_guilds = find2['movie_guilds']
                            game_guilds = find2['game_guilds']
                            platto_guilds = find2['platto_guilds']
                            music_guilds = find2['music_guilds']
                            shop_guilds = find2['shop_guilds']

                    else:
                        tmp_guild = []
                        tmp_guild.append(guild_id)
                        collection_total.insert_one({'totality':1,"all_guilds":tmp_guild,"anime_guilds":[],"public_guilds":[],"development_guilds":[],"movie_guilds":[] , "game_guilds":[],"platto_guilds":[],"music_guilds":[] , 'shop_guilds':[]})

                    response3 = requests.get(f"https://discord.com/api/v6/guilds/{guild_id}/channels" , headers={
                        'Authorization': f"Bot MTI2Nzg1MzAwOTQ3NjM4Njg5Nw.GEngSz.sKoQgCseG1ySMunYaOBHGmbQ5H0xkp0zvwckns"
                    })

                    request.session['channel_details'] = response3.json()


                    channels_db=request.session['channel_details']
                    id_selected_channel = None
                    for i in channels_db:
                        if i['type'] == 0:
                            if i['name'] == request.POST['channels']:
                                id_selected_channel = i['id']
                    genres = []
                    tabadol_value = 0
                    if request.POST['category'] == "پابلیک":
                        genres.append(1)
                        public_guilds.append(guild_id)
                        collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        if guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})

                    elif request.POST['category'] == "موزیک":
                        genres.append(2)
                        music_guilds.append(guild_id)
                        collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        if guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in public_guilds:
                            public_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})


                    elif request.POST['category'] == "بازی":
                        genres.append(3)

                        game_guilds.append(guild_id)
                        collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        if guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})



                    elif request.POST['category'] == "پلاتو":
                        genres.append(4)

                        platto_guilds.append(guild_id)
                        collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        if guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})




                    elif request.POST['category'] == "انیمیشن":
                        genres.append(5)
                        anime_guilds.append(guild_id)

                        collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        if guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})




                    elif request.POST['category'] == "فیلم":
                        genres.append(6)
                        movie_guilds.append(guild_id)


                        collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        if guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        elif guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})



                    elif request.POST['category'] == "برنامه نویسی":
                        genres.append(7)
                        development_guilds.append(guild_id)


                        collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})
                        if guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in shop_guilds:
                            shop_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})




                    elif request.POST['category'] == "فروشگاه":
                        genres.append(8)
                        shop_guilds.append(guild_id)

                        collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})
                        if guild_id in platto_guilds:
                            platto_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})
                        elif guild_id in movie_guilds:
                            movie_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})
                        elif guild_id in anime_guilds:
                            anime_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})
                        elif guild_id in music_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})
                        elif guild_id in game_guilds:
                            game_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})
                        elif guild_id in public_guilds:
                            music_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})
                        elif guild_id in development_guilds:
                            development_guilds.remove(guild_id)
                            collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})



                    ######################tabadol values ###################

                    if request.POST['tabadol'] == "پابلیک":
                        print(66666666)
                        tabadol_value = 1
                    elif request.POST['tabadol'] == "موزیک":
                        tabadol_value = 2
                    elif request.POST['tabadol'] == "بازی":
                        tabadol_value = 3
                    elif request.POST['tabadol'] == "پلاتو":
                        tabadol_value = 4
                    elif request.POST['tabadol'] == "انیمیشن":
                        tabadol_value = 5
                    elif request.POST['tabadol'] == "فیلم":
                        tabadol_value = 6
                    elif request.POST['tabadol'] == "برنامه نویسی":
                        tabadol_value = 7
                    elif request.POST['tabadol'] == "فروشگاه":
                        tabadol_value = 8
                    elif request.POST['tabadol'] == "همه دسته ها":
                        print('555555555555')

                        tabadol_value = "all"


                    ########################################################
                    if id_selected_channel !=None:
                        collection.insert_one({"server_id":int(guild_id) , 'channel':int(id_selected_channel) ,'banner_body':request.POST['body_banner'] , 'banner_title':request.POST['title_banner'] , 'banner_link':request.POST['link_banner'] , 'genres':genres , "active":True , 'tabadol':str(tabadol_value) , "tabadol_channels":[] })

        except:
            pass
        if (find:=collection.find_one({'server_id':int(guild_id)})):
            body_banner = find['banner_body']
            title_banner = find['banner_title']
            link_banner = find['banner_link']
            channel_selected = find['channel']

            genres = find['genres'][0]
            tabadol = find['tabadol']

            is_true= True
            
            if tabadol == "1":
                tabadol= "پابلیک"

            elif tabadol == "2":
                tabadol="موزیک"
            elif tabadol == "3":
                tabadol="بازی"
            elif tabadol == "4":
                tabadol="پلاتو"
            elif tabadol == "5":
                tabadol= "انیمیشن"
            elif tabadol == "6":
                tabadol= "فیلم"
            elif tabadol == "7":
                tabadol= "برنامه نویسی"
            elif tabadol == "8":
                tabadol= "فروشگاه"
            elif tabadol == "all":
                tabadol = "همه دسته ها"
                

            ######################################### ژانر خود سرور
            if genres == 1:
                genres= "پابلیک"

            elif genres == 2:
                genres="موزیک"
            elif genres == 3:
                genres="بازی"
            elif genres == 4:
                genres="پلاتو"
            elif genres == 5:
                genres= "انیمیشن"
            elif genres == 6:
                genres= "فیلم"
            elif genres == 7:
                genres= "برنامه نویسی"
            elif genres == 8:
                genres= "فروشگاه"
            # elif genres == "all":
            #     genres = "همه دسته ها"

        if is_done == False:
            request.session['selected'] = request.POST['dropdown']
            selected_value = request.session['selected']
            guilds = request.session['servers']
            bot_guilds = request.session['bot_servers']
            my_temp_ids = {}
            for j in bot_guilds:
                for i in guilds:
                    if j['id'] == i['id']:
                        if i['owner'] == True:
                            my_temp_ids[f"{i['name']}"] = i['id']
            
            guild_id = my_temp_ids[f'{selected_value}']
        
        response3 = requests.get(f"https://discord.com/api/v6/guilds/{guild_id}/channels" , headers={
            'Authorization': f"Bot MTI2Nzg1MzAwOTQ3NjM4Njg5Nw.GEngSz.sKoQgCseG1ySMunYaOBHGmbQ5H0xkp0zvwckns"
        })

        request.session['channel_details'] = response3.json()
        my_channels = response3.json()
        
        channels = {}
        
        for i in my_channels:
            if i['type'] == 0:
                channels[f"{i['name']}"] = i['id'] #{"parham":12345 , ...}

                try:
                    if int(i['id']) == channel_selected:
                        channel_selected_name = i['name']
                except:
                    pass


    guilds = request.session['servers']
    bot_guilds = request.session['bot_servers']
    my_temp_ids = {}
    for j in bot_guilds:
        for i in guilds:
            if j['id'] == i['id']:
                if i['owner'] == True:
                    my_temp_ids[f"{i['name']}"] = i['id']
    
    # print(my_temp_ids)
    if channel_selected_name != None and is_true== True:
        return render(request , 'profile.html' , context={"servers":my_temp_ids , "selected":selected_value , "channels":channels , "channel_selected":channel_selected_name , "body_banner":body_banner , "title_banner":title_banner , "link_banner":link_banner , "tabadol_lists":tabadol_lists , "genres_list" : genres_list , "current_genres":genres , "current_tabadol":tabadol})
        
    else:
        return render(request , 'profile.html' , context={"servers":my_temp_ids , "selected":selected_value , "channels":channels , "tabadol_lists":tabadol_lists , "genres_list" : genres_list})
