from django.db import models

class Whitelist_detial(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    evm = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    
    class Meta:
        db_table ="whitelist_Detail"     
        

class Whitelist_detial_1(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    evm_address = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    
    class Meta:
        db_table ="whitelist_Detail_1"           
    



    