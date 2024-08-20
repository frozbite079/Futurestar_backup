from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from eth_account.messages import encode_defunct
from eth_account import Account
from .models import *
import requests
import os 
import io
from PIL import Image 

from monsterapi import client
import base64 
import requests
import random

def dashboard(request):
    
    
    return  render(request,"/home/om/Downloads/crypto_project-1/static/html/dashboard.html")

@csrf_exempt
def MetaMaskUser(request):
    
    if request.method == "POST":
        data = json.loads(request.body)
        address = data.get('address')
        signature = data.get('signature')
        message = data.get('message')
        
        
                    
        message_hash = encode_defunct(text=message)
        
        recovered_address = Account.recover_message(message_hash, signature=signature)

        if recovered_address.lower() == address.lower():
            user, created = User.objects.get_or_create(username=address)
            
            user_addr = MetaUsers.objects.filter(address=str(address)).exists()
        
            if user_addr == True:
                user_nickname = MetaUsers.objects.get(address=str(address))
                
                return JsonResponse({'status': 'user_exist', 'redirect_url': 'UserDashboard','username':str(user_nickname.nickname),'user_id':str(user_nickname.user_id)})
                    
            else:

                return JsonResponse({'status': 'success', 'username': user.username})

        else:
            return JsonResponse({'status': 'error', 'message': 'Signature verification failed'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    
@csrf_exempt
def save_nickname_address(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nickname = data.get('nickname')
        address = data.get('address')

        '''API_URL = "https://api-inference.huggingface.co/models/alvdansen/phantasma-anime"
        headers = {"Authorization": "Bearer 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"}
        '''
        
        try:
            
            
            check_nickname = MetaUsers.objects.filter(nickname=nickname).exists()
            
            
            if check_nickname:
               
               return JsonResponse({'status': 'Exist'})
            else:
                try:
                    user = MetaUsers(
                    
                        address=address,nickname=nickname,coins=0,gems=0
                    ) 
                    user.save()
                    
                    get_user_id = MetaUsers.objects.get(address=address)
                    

                    directory = "/home/om/Downloads/crypto_project-1/static/profilepicture/"
                    
                    '''def query(payload):
                        response = requests.post(API_URL, headers=headers, json=payload)
                        
                        return response.content
                    image_bytes = query({
                        "inputs": "random anime character",
                    })
                    
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    save_name = str(nickname) + ".png"
                    image_name= os.path.join(directory,str(save_name))
                    image.save(image_name)'''
                    api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImY5Y2YxMTgyNjJlMDkyM2EzY2UyYjFjYjhiZmI2MGFmIiwiY3JlYXRlZF9hdCI6IjIwMjQtMDctMDRUMTE6NDM6MDIuMjM4OTkxIn0.pO5nxO6lX6P94GuH8jHJjhYS9ar1vtn3MEHxz8nCpQk'  
                    monster_client = client(api_key)

                    model = 'txt2img'  
                    random_seed = random.randint(1, 10000)  

                    input_data = {
                    'prompt': 'anime character (single color background) ',
                    'negprompt': 'deformed, bad anatomy, disfigured, poorly drawn face',
                    'samples': 1,
                    'steps': 50,
                    'aspect_ratio': 'square',
                    'guidance_scale': 7.5,
                    'seed': random_seed,
                                }
                    result = monster_client.generate(model, input_data)

                    image_filename = "generated_image.png"
                    image_data = result['output'][0]

                    if image_data.startswith("http"):
                        # Handle the case where it's a URL
                        image_filename = str(get_user_id.nickname)+".png"
                        response = requests.get(image_data)
                        with open(directory+image_filename, "wb") as f:
                            f.write(response.content)
                    else:
                        # Assuming it's base64, handle padding issues
                        missing_padding = len(image_data) % 4
                        if missing_padding:
                            image_data += '=' * (4 - missing_padding)

                        # Decode and save the base64 image
                        image_filename = str(get_user_id.nickname)+".png"
                        
                        with open(directory+image_filename, "wb") as f:
                            f.write(base64.b64decode(image_data))
                    return JsonResponse({'status':'success','redict_url': 'UserDashboard','username':nickname,"user_id":str(get_user_id.user_id)})

                except Exception as e:
                    
                    return JsonResponse({'status':str(e)})

                
                
                
                
            
            
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})    


def UserDashboard(request,username):
    
    '''if 'username' not in request.session or request.session['username'] != username:
        return  redirect("dashboard")
    '''
    
    image_path = str(username)+".png"
    
    user_content = MetaUsers.objects.get(nickname=username)
    
    context = {
        'username': username,
        'profile_picture' : image_path,
        'coins': user_content.coins,
        'gems': user_content.gems,
        'user_id': user_content.user_id,
    }

    return render(request,"/home/om/Downloads/crypto_project-1/static/html/user_dashboard.html",context)
    

def leaderboard(request,id):
    
    user_content = MetaUsers.objects.get(user_id=id)

    image_path = str(user_content.nickname)+".png"
    
    all_ranked_user = MetaUsers.objects.all()
    
    context = {
        'username': user_content.nickname,
        'profile_picture' : image_path,
        'coins': user_content.coins,
        'gems': user_content.gems,
        'rank': all_ranked_user,
        'user_id':user_content.user_id
        
        
    }
    return render(request,"/home/om/Downloads/crypto_project-1/static/html/Leaderboard.html",context)

def setttings(request,id):
    user_content = MetaUsers.objects.get(user_id=str(id))

    
    image_path = str(user_content.nickname)+".png"
    
    
    context = {
        'username': user_content.nickname,
        'profile_picture' : image_path,
        'coins': user_content.coins,
        'gems': user_content.gems,
        'user_id':user_content.user_id
        
        
    } 
    return render(request,"/home/om/Downloads/crypto_project-1/static/html/setting.html",context)

def changeusername(request):
    
    if request.method == "POST":
        try:
            
            data = json.loads(request.body)
            username = data.get('username')
            previous_name = data.get('previoususername')
            
            user = MetaUsers.objects.get(nickname = previous_name)
            
            user.nickname = username
            
            user.save()
            path_for_new = "/home/om/Downloads/crypto_project-1/static/profilepicture/"
            path = "/home/om/Downloads/crypto_project-1/static/profilepicture/"+str(previous_name)+".png"

            if os.path.exists(path):
                
                os.rename(path,path_for_new+username+".png")
                return JsonResponse({'status':'success'})

            else:
                print("error")
                return JsonResponse({'status':'error'})
        
        except Exception as e:
            print(e)
            return JsonResponse({'status':str(e)})
        

def  gameFrame(request,id):
    user_content = MetaUsers.objects.get(user_id=str(id))

    
    image_path = str(user_content.nickname)+".png"
    
    
    context = {
        'username': user_content.nickname,
        'profile_picture' : image_path,
        'coins': user_content.coins,
        'gems': user_content.gems,
        'user_id':user_content.user_id
        
        
    } 
    
    
    
    return render(request,"/home/om/Downloads/crypto_project-1/static/html/gameplay.html",context)    


@csrf_exempt
def updateGem(request):
    print("false")
    if request.method == 'POST':
        data = json.loads(request.body)
        gems = data.get('gems')
        user_id = data.get('user_id')
        print(gems)
        
        
        try:
            gem_save = MetaUsers.objects.get(user_id = user_id)
            
            print(str(gem_save.gems))
            
            gem_save.gems = gem_save.gems+1
            gem_save.save()
            
            
            
            return JsonResponse({'status':'updated','message':str(gem_save.gems)})

            
        except Exception as e:
            return JsonResponse({'status': 'error','message': str(e)}, status=400)
  

    
    
        


    return JsonResponse({'status': 'error','message': 'Invalid JSON'}, status=400)
@csrf_exempt
def coinadding(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        coin = data.get('coin')
        user_id = data.get('user_id')
        
        
        
        try:
            coin_save = MetaUsers.objects.get(user_id = user_id)
            
            print(str(coin_save.gems))
            
            coin_save.coins = coin_save.coins+coin
            coin_save.save()
            
            
            
            return JsonResponse({'status':'updated','message':str(coin_save.coins)})

            
        except Exception as e:
            return JsonResponse({'status': 'error','message': str(e)}, status=400)
  

    
    
        


    return JsonResponse({'status': 'error','message': 'Invalid JSON'}, status=400)
    
    

    
    
    
    
    
    
    

    
    
    
    
    
     
