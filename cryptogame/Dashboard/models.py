from django.db import models

class MetaUser(models.Model):
    address = models.CharField(max_length=200,unique=True,primary_key=True)
    nickname = models.CharField(max_length=200,unique=True)
    
    class Meta:
        db_table = "MetaUser" 
    