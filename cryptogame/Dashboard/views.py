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
                
                print(user_nickname.nickname)   
                return JsonResponse({'status': 'user_exist', 'redirect_url': 'UserDashboard','username':str(user_nickname.nickname)})
                    
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

        API_URL = "https://api-inference.huggingface.co/models/alvdansen/phantasma-anime"
        headers = {"Authorization": "Bearer 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"}

        
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
                    
                    directory = "/home/om/Downloads/crypto_project-1/static/profilepicture/"
                    
                    def query(payload):
                        response = requests.post(API_URL, headers=headers, json=payload)
                        
                        return response.content
                    image_bytes = query({
                        "inputs": "random anime character",
                    })
                    
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    save_name = str(nickname) + ".png"
                    image_name= os.path.join(directory,str(save_name))
                    image.save(image_name)
                    
                    return JsonResponse({'status':'success','redict_url': 'UserDashboard','username':nickname})

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
        'gems': user_content.gems
    }

    return render(request,"/home/om/Downloads/crypto_project-1/static/html/user_dashboard.html",context)
    

def leaderboard(request,username):
    
    image_path = str(username)+".png"
    
    user_content = MetaUsers.objects.get(nickname=username)
    all_ranked_user = MetaUsers.objects.all()
    
    context = {
        'username': username,
        'profile_picture' : image_path,
        'coins': user_content.coins,
        'gems': user_content.gems,
        'rank': all_ranked_user
        
    }
    return render(request,"/home/om/Downloads/crypto_project-1/static/html/Leaderboard.html",context)

def setttings(request,username):
    
    
    image_path = str(username)+".png"
    
    user_content = MetaUsers.objects.get(nickname=username)
    
    context = {
        'username': username,
        'profile_picture' : image_path,
        'coins': user_content.coins,
        'gems': user_content.gems,
        
        
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
            path = "/home/om/Downloads/crypto_project-1/static/profilepicture/"+str(previous_name)+".png"

            if os.path.exists(path):
                
                os.rename(path,username+".png")
                return JsonResponse({'status':'success'})

            else:
                print("error")
                return JsonResponse({'status':'error'})
        
        except Exception as e:
            print(e)
            return JsonResponse({'status':str(e)})
        
    
