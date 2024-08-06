from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from eth_account.messages import encode_defunct
from eth_account import Account
from .models import *

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
            
            user_addr = MetaUser.objects.filter(address=str(address)).exists()
        
            if user_addr:
                    
                    user_nickname = MetaUser.objects.get(address=address)
                    

            
            
            
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

        print(data)
        
        try:
            
            
            check_nickname = MetaUser.objects.filter(nickname=nickname).exists()
            
            if check_nickname:
               
               return JsonResponse({'status': 'Exist'})
            else:
                
                user = MetaUser(
                
                    address=address,nickname=nickname
                ) 
                user.save()
            
            
                return JsonResponse({'status': 'success','nickname':str(nickname)})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})    