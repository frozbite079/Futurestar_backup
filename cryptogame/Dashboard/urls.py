from django.urls import path
from .views import dashboard,MetaMaskUser,save_nickname_address,UserDashboard


urlpatterns = [
    path('metamask-login',dashboard,name="Dashboard"),
    path('MetaMaskUser',MetaMaskUser,name="Meta-Login"),
    path('saveUserdata',save_nickname_address,name="saveUserData"),
    path('UserDashboard/<username>',UserDashboard,name="UserDashboard")
]
