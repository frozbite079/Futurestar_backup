from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from . import models
def login(request):
    

    return render(request,'/workspaces/crypto_project/static/html/login.html')


def whitelist(request):
    

    return render(request,'whitelist.html')

@csrf_exempt
def storeuser(request):
    
    if request.method == "POST":

        
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        evm = request.POST.get('evm')
        reason = request.POST.get('reason')
        
        try:
            dom = models.Whitelist_detial_1.objects.filter(email =str(email)).exists()
            
            if dom == True:
                return JsonResponse({'status':'error','message':'Email is Already exist!'})
            elif dom == False:
                
                try:
                    whitelist_detial = models.Whitelist_detial_1(username =str(name),email=str(email),evm_address = str(evm),reason = str(reason))
                    
                    whitelist_detial.save()
                    
                    return JsonResponse({'status':'success'})

                    #return render(request,'whitelistregcomp.html')
                

                except Exception as e:
                    print(str(e))    
        except Exception as e:
            print(str(e))  
        return render(request, 'whitelist.html')

              
def whitelistsuccess(request):
    
    return render(request,"whitelistregcomp.html")
        
        
 

