from django.db import models

class MetaUsers(models.Model):
    user_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=200,unique=True)
    nickname = models.CharField(max_length=200,unique=True)
    coins = models.BigIntegerField()
    gems = models.BigIntegerField()
    class Meta:
        db_table = "MetaUsers" 
    