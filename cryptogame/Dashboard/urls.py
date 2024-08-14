from django.urls import path
from .views import dashboard,MetaMaskUser,save_nickname_address,UserDashboard,leaderboard,setttings,changeusername , gameFrame


urlpatterns = [
    path('metamask-login',dashboard,name="Dashboard"),
    path('MetaMaskUser',MetaMaskUser,name="Meta-Login"),
    path('saveUserdata',save_nickname_address,name="saveUserData"),
    path('UserDashboard/<username>',UserDashboard,name="UserDashboard"),
    path('leaderboard/<id>',leaderboard,name="leaderboard"),
    path('setting/<id>',setttings,name="setting"),
    path('usernamechange',changeusername,name="usernamechange"),
    path('gameframe/<id>',gameFrame,name="gameframe")
    
    
]
