from django.db import models

class MetaUser(models.Model):
    address = models.CharField(max_length=200,unique=True,primary_key=True)
    nickname = models.CharField(max_length=200,unique=True)
    coins = models.BigIntegerField()
    gems = models.BigIntegerField()
    class Meta:
        db_table = "MetaUser" 
    